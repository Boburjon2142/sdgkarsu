import "./globals.css";
import { Navigation } from "../components/navigation";


export const metadata = {
  title: "Secure MVP",
  description: "Production-structured Next.js frontend for a Django REST backend.",
};


export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navigation />
        <main className="container">{children}</main>
      </body>
    </html>
  );
}
