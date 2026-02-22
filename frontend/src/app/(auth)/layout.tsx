export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen items-center justify-center p-4">
            {/* Decorative background */}
            <div className="absolute inset-0 z-0 bg-background overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-brand-900/30 via-background to-background"></div>
            </div>

            <div className="relative z-10 w-full max-w-md">
                {children}
            </div>
        </div>
    );
}
