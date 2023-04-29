import ProjectBox from "@/components/ProjectBox";
import getConfig from "next/config";
import Link from "next/link";
import React, { useState } from "react";

const { publicRuntimeConfig } = getConfig();
const baseRestUrl = publicRuntimeConfig.baseRestUrl;

type ComponentProps = {
  projects: [
    {
      name: string;
      critical_vulnerabilities?: number;
      high_vulnerabilities?: number;
      medium_vulnerabilities?: number;
      low_vulnerabilities?: number;
    }
  ];
};

function Projects(props: ComponentProps) {
  return (
    <main className="w-full h-full p-2">
      <div className="w-full my-5 px-5 flex items-center">
        <div className="flex">
          <ul>
            <li className="flex border-2 rounded-full items-center px-3 py-1">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4 mr-1"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"
                  clipRule="evenodd"
                />
              </svg>
              <p className="ml-1 text-sm">add filter</p>
            </li>
          </ul>
        </div>
        <div className="ml-auto flex items-center">
          <div className="border-2 rounded-full flex items-center mx-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4 mx-2"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clipRule="evenodd"
              />
            </svg>
            <input
              id="search"
              type="text"
              placeholder="Search projects"
              className="focus:outline-none text-base mr-3"
            />
          </div>
          <button className="bg-blue-500 w-30 px-2 py-1 my-2 flex items-center text-sm rounded text-white">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            Add project
          </button>
        </div>
      </div>

      <ul className="w-full h-full">
        {props.projects.map((project) => (
          <li key={project.name}>
            <ProjectBox
              key={project.name}
              name={project.name}
              critical_vulnerabilities={project.critical_vulnerabilities ?? 0}
              high_vulnerabilities={project.high_vulnerabilities ?? 0}
              medium_vulnerabilities={project.medium_vulnerabilities ?? 0}
              low_vulnerabilities={project.low_vulnerabilities ?? 0}
            />
          </li>
        ))}
      </ul>
    </main>
  );
}

export async function getStaticProps() {
  const res = await fetch(`${baseRestUrl}/projects/summary`);
  const projects = await res.json();

  return {
    props: {
      projects,
    },
  };
}

export default Projects;
