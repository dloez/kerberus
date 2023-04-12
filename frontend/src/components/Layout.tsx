import React, { PropsWithChildren } from "react";
import Sidebar from "./Sidebar";
import Main from "./Main";

const Layout = ({ children }: PropsWithChildren) => {
  return (
    <div className="flex">
      <Sidebar />
      <Main />
      {children}
    </div>
  );
};
export default Layout;
