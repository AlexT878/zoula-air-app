import { UI_TEXT } from "@/constants/text";

export function Hero() {
  const { hero } = UI_TEXT;

  return (
    <section className="relative h-screen w-full overflow-hidden bg-primary">
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat transition-transform duration-700 hover:scale-105"
        style={{
          backgroundImage:
            "url(https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1600&q=80)",
        }}
      />

      <div className="absolute inset-0 bg-black/40" />

      <div className="relative z-10 h-full flex items-center justify-center container mx-auto px-6">
        <div className="text-center">
          <span className="text-white/40 text-xs font-black tracking-[0.3em] uppercase">
            {hero?.badge || "ZOULA AIR ZONE"}
          </span>
        </div>
      </div>
    </section>
  );
}
