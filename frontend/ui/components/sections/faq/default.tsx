import Link from "next/link";
import { ReactNode } from "react";
import { siteConfig } from "@/config/site"; // Make sure this path matches your project
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "../../ui/accordion";
import { Section } from "../../ui/section";

interface FAQItemProps {
  question: string;
  answer: ReactNode;
  value?: string;
}

interface FAQProps {
  title?: string;
  items?: FAQItemProps[] | false;
  className?: string;
}

export default function FAQ({
  title = "System Capabilities",
  items = [
    {
      question: "How is the trend data calculated?",
      answer: (
        <p className="text-muted-foreground mb-4 max-w-[640px] text-balance">
          We utilize real-time computer vision pipelines running on edge devices (Raspberry Pi). 
          Video feeds are processed to extract crowd density, movement vectors, and object interaction rates, 
          which are then aggregated into our trend visualization engine.
        </p>
      ),
    },
    {
      question: "Is the data truly real-time?",
      answer: (
        <p className="text-muted-foreground mb-4 max-w-[600px]">
          Yes. The system uses a low-latency MJPEG stream for visual verification and 
          websockets for data transmission. The typical latency between an event occurring 
          and it appearing on the trend graph is under 200 milliseconds.
        </p>
      ),
    },
    {
      question: "What hardware is required for deployment?",
      answer: (
        <>
          <p className="text-muted-foreground mb-4 max-w-[580px]">
            The system is designed to be hardware-agnostic, but optimized for ARM-based 
            edge computing.
          </p>
          <p className="text-muted-foreground mb-4 max-w-[640px] text-balance">
            Currently deployed on Raspberry Pi 4/5 units with standard camera modules. 
            The central processing and dashboarding can run on any standard Linux server or cloud instance.
          </p>
        </>
      ),
    },
    {
      question: "Can I export the trend reports?",
      answer: (
        <p className="text-muted-foreground mb-4 max-w-[580px]">
          All data points are stored in MongoDB and can be exported as CSV or JSON 
          for further analysis in tools like R, Python Pandas, or Excel.
        </p>
      ),
    },
  ],
  className,
}: FAQProps) {
  return (
    <Section className={className}>
      <div className="max-w-container mx-auto flex flex-col items-center gap-8">
        <h2 className="text-center text-3xl font-semibold sm:text-5xl">
          {title}
        </h2>
        {items !== false && items.length > 0 && (
          <Accordion type="single" collapsible className="w-full max-w-[800px]">
            {items.map((item, index) => (
              <AccordionItem
                key={index}
                value={item.value || `item-${index + 1}`}
              >
                <AccordionTrigger>{item.question}</AccordionTrigger>
                <AccordionContent>{item.answer}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        )}
      </div>
    </Section>
  );
}