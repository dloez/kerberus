import React from "react";
import Image from "next/image";
import { useRouter } from "next/router";
import Link from "next/link";

const Sidebar = () => {
  const { pathname } = useRouter();

  return (
    <aside
      className={`flex-none h-screen sticky top-0 w-20 transition ${
        pathname.includes("project/[name]") ? "sm:w-20" : "sm:w-64"
      }`}
    >
      <div className="bg-dark-navy-blue h-full w-full text-white p-1 flex flex-col">
        <div id="branding" className="p-3 pb-4 my-4">
          <Link href="/">
            <span></span>
            <div>
              <p
                className={`text-xl font-bold invisible transition ${
                  pathname.includes("project/[name]")
                    ? "sm:invisible"
                    : "sm:visible"
                }`}
              >
                Kerberus
              </p>
            </div>
          </Link>
        </div>
        <div id="links">
          <ul>
            <li>
              <Link href="/dashboard">
                <div
                  className={`flex items-center mr-3 ml-3 mb-1 p-3 hover:bg-steel-blue transition rounded-xl ${
                    pathname === "/dashboard" ? "bg-steel-blue" : ""
                  }`}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-[1.3rem] w-[1.3rem] ml-[0.1rem]"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                  <p
                    className={`text-sm font-medium ml-3 hidden transition ${
                      pathname.includes("project/[name]")
                        ? "sm:hidden"
                        : "sm:flex"
                    }`}
                  >
                    Dashboard
                  </p>
                </div>
              </Link>
            </li>
            <li>
              <Link href="/projects">
                <div
                  className={`flex items-center mx-3 mb-1 p-3 hover:bg-steel-blue transition rounded-xl ${
                    pathname.includes("/project") ? "bg-steel-blue" : ""
                  }`}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-[1.3rem] w-[1.3rem] ml-[0.1rem]"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
                    />
                  </svg>
                  <p
                    className={`text-sm font-medium ml-3 hidden transition ${
                      pathname.includes("project/[name]")
                        ? "sm:hidden"
                        : "sm:flex"
                    }`}
                  >
                    Projects
                  </p>
                </div>
              </Link>
            </li>
            <li>
              <Link href="/licenses">
                <div
                  className={`flex items-center mx-3 mb-1 p-3 hover:bg-steel-blue transition rounded-xl ${
                    pathname === "/licenses" ? "bg-steel-blue" : ""
                  }`}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-[1.3rem] w-[1.3rem] ml-[0.1rem]"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V16h2a1 1 0 110 2H7a1 1 0 110-2h2V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <p
                    className={`text-sm font-medium ml-3 hidden transition ${
                      pathname.includes("project/[name]")
                        ? "sm:hidden"
                        : "sm:flex"
                    }`}
                  >
                    Licenses
                  </p>
                </div>
              </Link>
            </li>
            <li>
              <Link href="/vulnerabilities">
                <div
                  className={`flex items-center mx-3 mb-1 p-3 hover:bg-steel-blue transition rounded-xl ${
                    pathname === "/vulnerabilities" ? "bg-steel-blue" : ""
                  }`}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-[1.3rem] w-[1.3rem] ml-[0.1rem]"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                    />
                  </svg>
                  <p
                    className={`text-sm font-medium ml-3 hidden transition ${
                      pathname.includes("project/[name]")
                        ? "sm:hidden"
                        : "sm:flex"
                    }`}
                  >
                    Vulnerabilities
                  </p>
                </div>
              </Link>
            </li>
            <li>
              <Link href="/organizations">
                <div
                  className={`flex items-center mx-3 mb-1 p-3 hover:bg-steel-blue transition rounded-xl ${
                    pathname === "/organizations" ? "bg-steel-blue" : ""
                  }`}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-[1.3rem] w-[1.3rem] ml-[0.1rem]"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <p
                    className={`text-sm font-medium ml-3 hidden transition ${
                      pathname.includes("project/[name]")
                        ? "sm:hidden"
                        : "sm:flex"
                    }`}
                  >
                    Organizations
                  </p>
                </div>
              </Link>
            </li>
          </ul>
        </div>
        <div id="bottom" className="mt-auto">
          <div className="flex items-center mx-3 p-3 mb-3 hover:bg-steel-blue transition rounded-xl">
            <div id="link-icon" className="mr-3">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-[1.3rem] w-[1.3rem] ml-[0.1rem]"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
            </div>
            <p
              className={`text-sm font-medium ml-3 hidden transition ${
                pathname.includes("project/[name]") ? "sm:hidden" : "sm:flex"
              }`}
            >
              Settings
            </p>
          </div>
          <div
            id="user"
            className="m-2 ml-3 pt-5 flex items-center border-t-[1.5px] border-white"
          >
            <div className="h-10 w-10 ml-1">
              <Image
                src="https://i.pravatar.cc/100"
                alt=""
                width="100"
                height="100"
                className="rounded-full"
              />
            </div>
            <div
              className={`flex flex-col justify-between hidden transition ${
                pathname.includes("project/[name]") ? "sm:hidden" : "sm:flex"
              }`}
            >
              <p className="ml-3 text-xs">Jane Doe</p>
              <p className="ml-3 text-xs">jane.doe@example.com</p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};
export default Sidebar;
