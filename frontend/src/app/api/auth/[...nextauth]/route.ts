import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import GithubProvider from "next-auth/providers/github";
import CredentialsProvider from "next-auth/providers/credentials";

const handler = NextAuth({
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID || "",
            clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
        }),
        GithubProvider({
            clientId: process.env.GITHUB_CLIENT_ID || "",
            clientSecret: process.env.GITHUB_CLIENT_SECRET || "",
        }),
        CredentialsProvider({
            name: "Credentials",
            credentials: {
                email: { label: "Email", type: "email" },
                password: { label: "Password", type: "password" }
            },
            async authorize(credentials) {
                // Email/password auth is handled directly via authStore and Axios,
                // this is a fallback if someone uses signIn("credentials")
                if (credentials?.email === "admin@example.com" && credentials?.password === "password") {
                    return { id: "1", name: "Admin", email: "admin@example.com" };
                }
                return null;
            }
        })
    ],
    pages: {
        signIn: '/login',
    },
    callbacks: {
        async signIn({ account, user }) {
            // When user signs in with OAuth, we don't want NextAuth to create a session immediately.
            // We want to send the access_token (or code depending on provider setup) to our backend.
            // For simpler integration, if we have account.access_token from Google/Github,
            // we could send that. However, our FastAPI backend expects `code`.
            // Note: NextAuth abstract this away. A simpler way in Next.js + external API:
            // Intercept the token here, but the standard flow for external backends is often
            // to have the frontend redirect to the backend directly.
            // We'll let NextAuth proceed here, but we will pass the tokens in the `jwt` callback.
            return true;
        },
        async jwt({ token, account }) {
            // If it's the first sign in (account is available)
            if (account && account.provider !== 'credentials') {
                try {
                    // In a production scenario, you'd exchange the OAuth id_token or access_token
                    // with your backend here. Because our backend expects a standard OAuth
                    // `code` (which NextAuth already consumed), we must adjust our strategy.
                    // For now, we will assume NextAuth manages the OAuth session.
                    token.accessToken = account.access_token;
                    token.provider = account.provider;
                } catch (error) {
                    console.error("Error exchanging token with backend:", error);
                }
            }
            return token;
        },
        async session({ session, token }) {
            // Expose the access token to the client side
            (session as any).accessToken = token.accessToken;
            (session as any).provider = token.provider;
            return session;
        }
    },
    session: {
        strategy: "jwt",
    },
});

export { handler as GET, handler as POST };

