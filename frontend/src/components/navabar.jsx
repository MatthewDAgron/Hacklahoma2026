import React, { useState, useRef, useEffect } from "react";
import { NavLink } from "react-router-dom";
import { Camera, LayoutDashboard, User, Settings, LogOut } from "lucide-react";

const Navbar = () => {
  const [profileOpen, setProfileOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setProfileOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const linkBase =
    "flex items-center gap-2 px-4 py-2 rounded-lg transition";

  const linkInactive = "text-white/70 hover:text-white";
  const linkActive = "text-white bg-white/10";

  return (
    <nav className="w-full h-16 bg-transparent border-b border-white/10 flex items-center justify-between px-6">
      {/* LEFT - Logo */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 flex items-center justify-center font-bold text-white">
        </div>
        <span className="text-white text-lg font-semibold">
          Slacker
        </span>
      </div>

      {/* CENTER - Navigation */}
      <div className="flex items-center gap-4">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `${linkBase} ${isActive ? linkActive : linkInactive}`
          }
        >
          <LayoutDashboard size={20} />
          Dashboard
        </NavLink>

        <button className={`${linkBase} ${linkInactive}`}>
          <Camera size={20} />
          Camera
        </button>
      </div>

      {/* RIGHT - Profile with dropdown */}
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setProfileOpen(!profileOpen)}
          className={`${linkBase} ${linkInactive}`}
        >
          <User size={20} />
          Profile
        </button>

        {profileOpen && (
          <div className="absolute right-0 top-full mt-2 w-48 py-1 bg-[#0f172a] border border-white/10 rounded-lg shadow-xl z-50">
            <NavLink
              to="/profile"
              onClick={() => setProfileOpen(false)}
              className="flex items-center gap-2 px-4 py-2.5 text-white/80 hover:bg-white/10 hover:text-white transition"
            >
              <User size={18} />
              Profile
            </NavLink>
            <NavLink
              to="/settings"
              onClick={() => setProfileOpen(false)}
              className="flex items-center gap-2 px-4 py-2.5 text-white/80 hover:bg-white/10 hover:text-white transition"
            >
              <Settings size={18} />
              Settings
            </NavLink>
            <button
              onClick={() => {
                setProfileOpen(false);
                // Add logout logic here (e.g. clear auth, redirect)
              }}
              className="flex items-center gap-2 w-full px-4 py-2.5 text-white/80 hover:bg-white/10 hover:text-white transition text-left"
            >
              <LogOut size={18} />
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
