import { UI_TEXT } from "@/constants/text";
import SearchForm from "./SearchForm/SearchForm";

export function Hero() {
  const { hero } = UI_TEXT;

  return (
    <section className="relative h-screen w-full overflow-hidden bg-primary">
      {/* Background & Overlay */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat transition-transform duration-700 hover:scale-105"
        style={{
          backgroundImage: "url('/images/background.jpeg')",
        }}
      />
      <div className="absolute inset-0 bg-black/40" />

      {/* Content Container */}
      <div className="relative z-10 h-full flex flex-col items-center justify-center container mx-auto px-6">
        <div className="text-center mb-10">
          <h1 className="text-white text-5xl md:text-7xl font-bold tracking-tight mb-4">
            {hero.title}
          </h1>
          <p className="text-white/80 text-xl md:text-2xl max-w-2xl mx-auto font-light">
            {hero.subTitle}
          </p>
        </div>
        <SearchForm />
      </div>
    </section>
  );
}
