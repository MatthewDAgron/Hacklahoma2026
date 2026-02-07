import React from "react";

const DashboardCard = ({ title, value, icon, change }) => {
  return (
    <div
      className="
        w-[280px]
        h-[279px]
        rounded-[1rem]
        bg-[linear-gradient(135deg,#0ea5e9_0%,#2563eb_50%,#1e3a8a_100%)]
        shadow-[rgba(56,189,248,0.35)_0px_-23px_25px_0px_inset,
                 rgba(14,165,233,0.3)_0px_-36px_30px_0px_inset,
                 rgba(2,132,199,0.25)_0px_-79px_40px_0px_inset,
                 rgba(56,189,248,0.25)_0px_2px_1px,
                 rgba(56,189,248,0.3)_0px_4px_2px,
                 rgba(56,189,248,0.3)_0px_8px_4px,
                 rgba(56,189,248,0.3)_0px_16px_8px,
                 rgba(56,189,248,0.3)_0px_32px_16px]
        p-6
        flex
        flex-col
        text-white
        transition-all
        duration-300
        hover:scale-105
      "
    >
      {/* Top Row */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-white/70 text-sm font-medium">
          {title}
        </h3>
        <div className="text-white/80">
          {icon}
        </div>
      </div>

      {/* Centered Value */}
      <div className="flex-1 flex items-center justify-center">
        <h2 className="text-7xl font-bold text-white text-center tracking-wide">
          {value}
        </h2>
      </div>

      {/* Bottom Change Indicator */}
      {change && (
        <p className="text-sm text-cyan-200 text-center">
          {change}
        </p>
      )}
    </div>
  );
};

export default DashboardCard;
