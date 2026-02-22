"""SEO Scanner — meta tags, content structure, indexation, structured data, technical SEO."""
from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from app.scanners.base import BaseScanner, ScanCallback

logger = logging.getLogger(__name__)


class SEOScanner(BaseScanner):
    """Analyse SEO factors: meta tags, content, technical, mobile, indexation."""

    name = "seo"

    async def run(self, url: str, callback: ScanCallback) -> dict[str, Any]:
        """Execute all SEO checks against the target URL."""
        results: dict[str, Any] = {"url": url}

        try:
            async with httpx.AsyncClient(
                follow_redirects=True, timeout=15,
                headers={"User-Agent": "SynapsBranch SEO Scanner/1.0"}
            ) as client:
                response = await client.get(url)
        except Exception as exc:
            await callback({
                "type": "log", "phase": "seo", "level": "error",
                "message": f"Failed to fetch URL: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            results["error"] = str(exc)
            results["score"] = 0
            results["grade"] = "F"
            return results

        html = response.text
        headers = response.headers
        soup = BeautifulSoup(html, "lxml")

        # 1. Meta tags (20%)
        results["meta"] = await self._check_meta(soup, callback)

        # 2. Content structure (25%)
        results["content"] = await self._check_content(soup, callback)

        # 3. Technical (25%)
        results["technical"] = await self._check_technical(
            url, html, headers, response, callback
        )

        # 4. Mobile (15%)
        results["mobile"] = await self._check_mobile(soup, callback)

        # 5. Indexation (15%)
        results["indexation"] = await self._check_indexation(url, soup, callback)

        # 6. Structured data (bonus)
        results["structured_data"] = await self._check_structured_data(soup, callback)

        score = self.calculate_score(results)
        grade = self.calculate_grade(score)
        results["score"] = score
        results["grade"] = grade

        return results

    # ── Sub-checks ──

    async def _check_meta(self, soup: BeautifulSoup, callback: ScanCallback) -> dict[str, Any]:
        """Check title, meta description, canonical, robots, OG tags, Twitter Cards."""
        meta: dict[str, Any] = {"score": 100}

        # Title
        title_tag = soup.find("title")
        title_text = title_tag.get_text(strip=True) if title_tag else None
        meta["title"] = {"exists": title_text is not None, "text": title_text, "length": len(title_text) if title_text else 0}

        if not title_text:
            meta["score"] -= 25
            await callback({"type": "log", "phase": "seo", "level": "error", "message": "Missing <title> tag", "timestamp": datetime.now(timezone.utc).isoformat()})
        elif len(title_text) < 30 or len(title_text) > 60:
            meta["score"] -= 10
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"Title length ({len(title_text)} chars) outside optimal range (30-60)", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"Title tag present ({len(title_text)} chars)", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Meta description
        desc_tag = soup.find("meta", attrs={"name": "description"})
        desc_text = desc_tag.get("content", "").strip() if desc_tag else None
        meta["description"] = {"exists": desc_text is not None and len(desc_text) > 0, "text": desc_text, "length": len(desc_text) if desc_text else 0}

        if not desc_text:
            meta["score"] -= 20
            await callback({"type": "log", "phase": "seo", "level": "error", "message": "Missing meta description", "timestamp": datetime.now(timezone.utc).isoformat()})
        elif len(desc_text) < 120 or len(desc_text) > 160:
            meta["score"] -= 5
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"Meta description length ({len(desc_text)} chars) outside optimal range (120-160)", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"Meta description present ({len(desc_text)} chars)", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Canonical URL
        canonical = soup.find("link", rel="canonical")
        meta["canonical"] = {"exists": canonical is not None, "href": canonical.get("href") if canonical else None}
        if not canonical:
            meta["score"] -= 10
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": "Missing canonical URL", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"Canonical URL: {canonical.get('href')}", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Meta robots
        robots_tag = soup.find("meta", attrs={"name": "robots"})
        meta["robots"] = {"exists": robots_tag is not None, "content": robots_tag.get("content") if robots_tag else None}

        # Open Graph tags
        og_tags = {}
        for og_prop in ["og:title", "og:description", "og:image", "og:url", "og:type"]:
            tag = soup.find("meta", property=og_prop)
            og_tags[og_prop] = tag.get("content") if tag else None

        meta["open_graph"] = og_tags
        og_present = sum(1 for v in og_tags.values() if v)
        if og_present < 3:
            meta["score"] -= 10
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"Only {og_present}/5 Open Graph tags found", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"Open Graph tags: {og_present}/5 present", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Twitter Cards
        twitter_tags = {}
        for tw_name in ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]:
            tag = soup.find("meta", attrs={"name": tw_name})
            twitter_tags[tw_name] = tag.get("content") if tag else None

        meta["twitter_cards"] = twitter_tags
        tw_present = sum(1 for v in twitter_tags.values() if v)
        if tw_present < 2:
            meta["score"] -= 5

        meta["score"] = max(0, meta["score"])
        return meta

    async def _check_content(self, soup: BeautifulSoup, callback: ScanCallback) -> dict[str, Any]:
        """Check heading structure, image alt tags, link text."""
        content: dict[str, Any] = {"score": 100}

        # H1 check
        h1_tags = soup.find_all("h1")
        content["h1_count"] = len(h1_tags)
        content["h1_texts"] = [h1.get_text(strip=True)[:100] for h1 in h1_tags]

        if len(h1_tags) == 0:
            content["score"] -= 25
            await callback({"type": "log", "phase": "seo", "level": "error", "message": "No H1 tag found", "timestamp": datetime.now(timezone.utc).isoformat()})
        elif len(h1_tags) > 1:
            content["score"] -= 10
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"Multiple H1 tags found ({len(h1_tags)}). Use only one H1.", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"Single H1 tag: \"{h1_tags[0].get_text(strip=True)[:60]}\"", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Heading hierarchy
        heading_levels = []
        for level in range(1, 7):
            tags = soup.find_all(f"h{level}")
            heading_levels.append({"level": level, "count": len(tags)})

        content["headings"] = heading_levels
        hierarchy_ok = True
        prev_count = heading_levels[0]["count"] if heading_levels else 0
        for i in range(1, len(heading_levels)):
            if heading_levels[i]["count"] > 0 and heading_levels[i - 1]["count"] == 0:
                hierarchy_ok = False
                break

        content["hierarchy_valid"] = hierarchy_ok
        if not hierarchy_ok:
            content["score"] -= 10
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": "Heading hierarchy has gaps (e.g. H1 -> H3 without H2)", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": "Heading hierarchy is valid", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Image alt attributes
        images = soup.find_all("img")
        images_without_alt = [img.get("src", "")[:100] for img in images if not img.get("alt")]
        content["total_images"] = len(images)
        content["images_without_alt"] = len(images_without_alt)

        if images and images_without_alt:
            pct = len(images_without_alt) / len(images) * 100
            content["score"] -= min(20, int(pct / 5))
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"{len(images_without_alt)}/{len(images)} images missing alt attribute", "timestamp": datetime.now(timezone.utc).isoformat()})
        elif images:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"All {len(images)} images have alt attributes", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Links without descriptive text
        links = soup.find_all("a", href=True)
        generic_texts = {"click here", "here", "read more", "more", "link"}
        bad_links = [
            a for a in links
            if a.get_text(strip=True).lower() in generic_texts
        ]
        content["total_links"] = len(links)
        content["non_descriptive_links"] = len(bad_links)

        if bad_links:
            content["score"] -= min(10, len(bad_links) * 2)
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"{len(bad_links)} link(s) with non-descriptive text", "timestamp": datetime.now(timezone.utc).isoformat()})

        content["score"] = max(0, content["score"])
        return content

    async def _check_technical(
        self, url: str, html: str, headers: httpx.Headers, response: httpx.Response, callback: ScanCallback
    ) -> dict[str, Any]:
        """Check compression, page size, minification."""
        tech: dict[str, Any] = {"score": 100}

        # Compression
        content_encoding = headers.get("content-encoding", "").lower()
        has_compression = content_encoding in ("gzip", "br", "deflate")
        tech["compression"] = {"enabled": has_compression, "encoding": content_encoding}

        if not has_compression:
            tech["score"] -= 15
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": "No compression (Gzip/Brotli) detected", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"Compression enabled: {content_encoding}", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Page size
        page_size_kb = len(html.encode("utf-8")) / 1024
        tech["page_size_kb"] = round(page_size_kb, 2)

        if page_size_kb > 500:
            tech["score"] -= 20
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"Large page size: {page_size_kb:.0f} KB", "timestamp": datetime.now(timezone.utc).isoformat()})
        elif page_size_kb > 200:
            tech["score"] -= 10
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"Page size: {page_size_kb:.0f} KB (consider optimizing)", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"Page size: {page_size_kb:.0f} KB", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Response time
        tech["response_time_ms"] = response.elapsed.total_seconds() * 1000 if response.elapsed else None

        # Check CSS/JS minification (heuristic: check for excessive whitespace)
        soup = BeautifulSoup(html, "lxml")
        inline_scripts = soup.find_all("script", src=False)
        unminified_scripts = 0
        for script in inline_scripts:
            text = script.get_text()
            if text and len(text) > 200:
                lines = text.strip().split("\n")
                if len(lines) > 10:
                    unminified_scripts += 1

        tech["unminified_inline_scripts"] = unminified_scripts
        if unminified_scripts > 0:
            tech["score"] -= 5
            await callback({"type": "log", "phase": "seo", "level": "info", "message": f"{unminified_scripts} inline script(s) appear unminified", "timestamp": datetime.now(timezone.utc).isoformat()})

        tech["score"] = max(0, tech["score"])
        return tech

    async def _check_mobile(self, soup: BeautifulSoup, callback: ScanCallback) -> dict[str, Any]:
        """Check viewport meta tag and mobile-friendliness indicators."""
        mobile: dict[str, Any] = {"score": 100}

        # Viewport
        viewport = soup.find("meta", attrs={"name": "viewport"})
        mobile["viewport"] = {"exists": viewport is not None, "content": viewport.get("content") if viewport else None}

        if not viewport:
            mobile["score"] -= 40
            await callback({"type": "log", "phase": "seo", "level": "error", "message": "Missing viewport meta tag (critical for mobile)", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            content = viewport.get("content", "")
            if "width=device-width" in content:
                await callback({"type": "log", "phase": "seo", "level": "success", "message": "Viewport meta tag configured correctly", "timestamp": datetime.now(timezone.utc).isoformat()})
            else:
                mobile["score"] -= 15
                await callback({"type": "log", "phase": "seo", "level": "warning", "message": f"Viewport configuration may not be optimal: {content}", "timestamp": datetime.now(timezone.utc).isoformat()})

        # Check for media queries (basic heuristic)
        style_tags = soup.find_all("style")
        has_media_queries = any("@media" in style.get_text() for style in style_tags)
        mobile["has_media_queries_inline"] = has_media_queries

        mobile["score"] = max(0, mobile["score"])
        return mobile

    async def _check_indexation(
        self, url: str, soup: BeautifulSoup, callback: ScanCallback
    ) -> dict[str, Any]:
        """Check robots.txt, sitemap.xml, noindex/nofollow directives."""
        index: dict[str, Any] = {"score": 100}
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        # robots.txt
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                robots_resp = await client.get(f"{base}/robots.txt")
            if robots_resp.status_code == 200:
                index["robots_txt"] = {"exists": True, "content": robots_resp.text[:2000]}
                await callback({"type": "log", "phase": "seo", "level": "success", "message": "robots.txt found", "timestamp": datetime.now(timezone.utc).isoformat()})
            else:
                index["robots_txt"] = {"exists": False}
                index["score"] -= 10
                await callback({"type": "log", "phase": "seo", "level": "warning", "message": "robots.txt not found", "timestamp": datetime.now(timezone.utc).isoformat()})
        except Exception:
            index["robots_txt"] = {"exists": False, "error": "fetch failed"}
            index["score"] -= 10

        # sitemap.xml
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                sitemap_resp = await client.get(f"{base}/sitemap.xml")
            if sitemap_resp.status_code == 200 and "xml" in sitemap_resp.headers.get("content-type", ""):
                index["sitemap"] = {"exists": True}
                await callback({"type": "log", "phase": "seo", "level": "success", "message": "sitemap.xml found", "timestamp": datetime.now(timezone.utc).isoformat()})
            else:
                index["sitemap"] = {"exists": False}
                index["score"] -= 15
                await callback({"type": "log", "phase": "seo", "level": "warning", "message": "sitemap.xml not found or invalid", "timestamp": datetime.now(timezone.utc).isoformat()})
        except Exception:
            index["sitemap"] = {"exists": False, "error": "fetch failed"}
            index["score"] -= 15

        # noindex / nofollow
        robots_meta = soup.find("meta", attrs={"name": "robots"})
        if robots_meta:
            content = robots_meta.get("content", "").lower()
            index["noindex"] = "noindex" in content
            index["nofollow"] = "nofollow" in content
            if index["noindex"]:
                index["score"] -= 30
                await callback({"type": "log", "phase": "seo", "level": "error", "message": "Page has noindex directive — will not be indexed", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            index["noindex"] = False
            index["nofollow"] = False

        index["score"] = max(0, index["score"])
        return index

    async def _check_structured_data(
        self, soup: BeautifulSoup, callback: ScanCallback
    ) -> dict[str, Any]:
        """Check for JSON-LD and microdata structured data."""
        structured: dict[str, Any] = {}

        # JSON-LD
        json_ld_scripts = soup.find_all("script", type="application/ld+json")
        structured["json_ld_count"] = len(json_ld_scripts)
        structured["json_ld_types"] = []
        for script in json_ld_scripts:
            try:
                import json
                data = json.loads(script.string or "")
                if isinstance(data, dict):
                    structured["json_ld_types"].append(data.get("@type", "unknown"))
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            structured["json_ld_types"].append(item.get("@type", "unknown"))
            except Exception:
                pass

        # Microdata
        microdata_items = soup.find_all(attrs={"itemtype": True})
        structured["microdata_count"] = len(microdata_items)

        total = structured["json_ld_count"] + structured["microdata_count"]
        if total > 0:
            await callback({"type": "log", "phase": "seo", "level": "success", "message": f"Structured data found: {structured['json_ld_count']} JSON-LD, {structured['microdata_count']} microdata", "timestamp": datetime.now(timezone.utc).isoformat()})
        else:
            await callback({"type": "log", "phase": "seo", "level": "warning", "message": "No structured data (JSON-LD or microdata) found", "timestamp": datetime.now(timezone.utc).isoformat()})

        return structured

    # ── Scoring ──

    def calculate_score(self, results: dict[str, Any]) -> int:
        """Weighted score: Meta 20%, Content 25%, Technical 25%, Mobile 15%, Indexation 15%."""
        meta_score = results.get("meta", {}).get("score", 0)
        content_score = results.get("content", {}).get("score", 0)
        tech_score = results.get("technical", {}).get("score", 0)
        mobile_score = results.get("mobile", {}).get("score", 0)
        index_score = results.get("indexation", {}).get("score", 0)

        weighted = (
            meta_score * 0.20
            + content_score * 0.25
            + tech_score * 0.25
            + mobile_score * 0.15
            + index_score * 0.15
        )
        return max(0, min(100, int(round(weighted))))
