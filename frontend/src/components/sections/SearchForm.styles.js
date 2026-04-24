import { cn } from "@/lib/utils";

const baseInput = "h-12 border-gray-300/80 placeholder:text-muted-foreground";
const focusStyles =
  "focus-visible:ring-0 focus-visible:border-gray-400/80 focus-visible:z-10";

export const styles = {
  card: "w-full max-w-6xl shadow-2xl border-none rounded-3xl bg-white/95 backdrop-blur-md",
  header: "pb-4 pt-4 px-8",
  content: "px-8 pb-8",

  tabList: "flex bg-transparent h-auto p-0 gap-2",
  tabTrigger: cn(
    "px-4 py-4 rounded-lg text-sm font-medium transition-all",
    "text-muted-foreground bg-transparent hover:bg-gray-200",
    "data-[state=active]:bg-primary data-[state=active]:text-primary-foreground data-[state=active]:shadow-sm",
  ),

  label: "text-xs uppercase font-bold text-slate-500 ml-1",

  inputDefault: cn(baseInput, focusStyles, "rounded-md"),
  inputSplitLeft: cn(
    baseInput,
    focusStyles,
    "rounded-r-none border-r-0 focus-visible:border-r",
  ),
  inputSplitRight: cn(baseInput, focusStyles, "rounded-l-none pl-4"),

  submitBtn: "w-full h-14 px-24 text-lg font-bold shadow-lg shadow-primary/30",
};
