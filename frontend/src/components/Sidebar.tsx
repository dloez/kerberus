import React from "react";
import Image from "next/image";
import { useRouter } from 'next/router';
import Link from 'next/link'

const Sidebar = () => {
  const {pathname} = useRouter();

  return (
    <div className="object-left flex-none h-screen w-64 absolute">
      <div className="bg-dark-navy-blue h-full w-full text-white font-varela-round p-1 flex flex-col">
        <div id="branding" className="m-3 p-3 pb-4 mb-4">
          <Link href="/">
            <span></span>
            <div>
              <p className="text-xl font-bold">Kerberus</p>
            </div>
          </Link>
        </div>
        <div id="links" className="grid grid-cols-1">
          <ul>
            <li>
              <Link href="/dashboard">
                <div className={`flex items-center mx-3 mb-1 p-3 hover:bg-steel-blue rounded-xl ${pathname === '/dashboard' ? 'bg-steel-blue' : '' }`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-[1.2rem] w-[1.2rem]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <p className="text-sm font-medium ml-3">Dashboard</p>
                </div>
              </Link>
            </li>
            <li>
              <Link href="/projects">
                <div className={`flex items-center mx-3 mb-1 p-3 hover:bg-steel-blue rounded-xl ${pathname === '/projects' ? 'bg-steel-blue' : '' }`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-[1.2rem] w-[1.2rem]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                  <p className="text-sm font-medium ml-3">Projects</p>
                </div>
              </Link>
            </li>
            <li>
              <Link href="/organizations">
                <div className={`flex items-center mx-3 mb-1 p-3 hover:bg-steel-blue rounded-xl ${pathname === '/organizations' ? 'bg-steel-blue' : '' }`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-[1.2rem] w-[1.2rem]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-sm font-medium ml-3">Organizations</p>
                </div>
              </Link>
            </li>
          </ul>
        </div>
        <div id="bottom" className="mt-auto">
          <div className="flex items-center mx-3 p-3 mb-3 hover:bg-steel-blue rounded-xl">
            <div id="link-icon" className="mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-[1.2rem] w-[1.2rem]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <p className="text-sm font-medium">Settings</p>
          </div>
          <div id="user" className="m-2 ml-3 pt-5 flex items-center border-t-[1.5px] border-white">
            <div className="h-10 w-10 content-center">
              <Image src="https://i.pravatar.cc/100" alt="" width="100" height="100" className="rounded-full"/>
            </div>
            <div className="flex flex-col justify-between">
              <p className="ml-3 text-xs">Jane Doe</p>
              <p className="ml-3 text-xs">jane.doe@example.com</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Sidebar;

