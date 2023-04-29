import React, { PropsWithChildren } from "react";
import Sidebar from "./Sidebar";

const Layout = ({ children }: PropsWithChildren) => {
  return (
    <div className="flex">
      <Sidebar />
      <div className="w-full h-full">{children}</div>
    </div>
  );
};
export default Layout;
