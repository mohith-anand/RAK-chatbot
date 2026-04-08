import { useState, useEffect } from "react";
import { motion, useScroll, useTransform } from "motion/react";
import ChatModal from "./components/ChatModal";
import { cn } from "./lib/utils";

export default function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const { scrollY } = useScroll();
  
  // Blur effect based on scroll
  const blurValue = useTransform(scrollY, [0, 500], [0, 20]);
  const blurFilter = useTransform(blurValue, (v) => `blur(${v}px)`);

  return (
    <main className="relative min-h-[200vh] bg-charcoal overflow-x-hidden selection:bg-gold/30">
      {/* Hero Section */}
      <section className="relative h-screen w-full flex flex-col items-center justify-center overflow-hidden">
        {/* Background Layer */}
        <motion.div 
          style={{ filter: blurFilter }}
          className="absolute inset-0 z-0 bg-full-image transition-all duration-300"
        >
          {/* Brown/Warm Editorial Filter Overlay */}
          <div className="absolute inset-0 bg-[#1d1b18]/65 mix-blend-multiply" />
          
          {/* Subtle Gradient for readability */}
          <div className="absolute inset-0 bg-gradient-to-b from-charcoal/40 via-transparent to-charcoal/80" />
          
          {/* Typography Glow */}
          <div className="absolute inset-0 radial-glow z-10 pointer-events-none" />
        </motion.div>

        {/* Content Center */}
        <div className="relative z-20 text-center max-w-4xl px-6 flex flex-col items-center justify-center h-full">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            className="flex flex-col items-center space-y-2"
          >
            <h1 className="font-headline font-light italic text-6xl md:text-8xl text-gold tracking-tight opacity-95">
              Defining the ground
            </h1>
            <h1 className="font-headline font-medium text-6xl md:text-8xl text-white tracking-tight opacity-100">
              you stand <span className="italic font-light text-gold">on.</span>
            </h1>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8, duration: 1.5 }}
            className="mt-12"
          >
            <button 
              onClick={() => setIsChatOpen(true)}
              className="group relative border border-gold/60 text-gold font-jost text-[12px] tracking-[0.4em] uppercase transition-all duration-700 overflow-hidden px-12 py-4 hover:bg-gold hover:text-charcoal"
            >
              <span className="relative z-10">Chat with AI</span>
            </button>
          </motion.div>
        </div>
      </section>

      {/* Empty scrollable expanse below the fold */}
      <div className="h-screen w-full bg-transparent pointer-events-none" />

      {/* Components */}
      <ChatModal 
        isOpen={isChatOpen} 
        onClose={() => setIsChatOpen(false)} 
      />
    </main>
  );
}
