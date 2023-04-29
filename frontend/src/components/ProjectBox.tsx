import React, { FunctionComponent, useState } from "react";
import Critical from "./icons/Critical";
import High from "./icons/High";
import Medium from "./icons/Medium";
import Low from "./icons/Low";
import Link from "next/link";

type ComponentProps = {
  name: string;
  critical_vulnerabilities?: number;
  high_vulnerabilities?: number;
  medium_vulnerabilities?: number;
  low_vulnerabilities?: number;
};

export enum IconStyle {
  Solid = "solid",
  Outline = "Outline",
}

const ProjectBox: FunctionComponent<ComponentProps> = (
  props: ComponentProps
) => {
  const [isHovering, setIsHovering] = useState(false);
  const [isChecked, setCheck] = useState(false);

  const handleCheck = () => {
    setCheck(!isChecked);
  };

  return (
    <div
      className="w-full p-2 my-2 border rounded mx-auto my-1 hover:border-dark-navy-blue flex items-center"
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      <div className="border-r-2 px-2 pr-4 min-w-fit">
        <input type="checkbox" onClick={handleCheck} />
      </div>
      <div className="flex w-[85%] min-w-[30%]">
        <Link href={`project/${props.name}`} className="px-[50%]">
          <p className="font-light text-sm w-full">{props.name}</p>
        </Link>
      </div>
      <div className="flex justify-between w-[15%] min-w-min border-l-2 pl-3">
        <div className="flex items-center">
          <p className="m-1 font-bold">{props.critical_vulnerabilities}</p>
          {isHovering ? (
            <Critical style={IconStyle.Solid} />
          ) : (
            <Critical style={IconStyle.Outline} />
          )}
        </div>
        <div className="flex items-center">
          <p className="m-1 font-bold">{props.high_vulnerabilities}</p>
          {isHovering ? (
            <High style={IconStyle.Solid} />
          ) : (
            <High style={IconStyle.Outline} />
          )}
        </div>
        <div className="flex items-center">
          <p className="m-1 font-bold">{props.medium_vulnerabilities}</p>
          {isHovering ? (
            <Medium style={IconStyle.Solid} />
          ) : (
            <Medium style={IconStyle.Outline} />
          )}
        </div>
        <div className="flex items-center">
          <p className="m-1 font-bold">{props.low_vulnerabilities}</p>
          {isHovering ? (
            <Low style={IconStyle.Solid} />
          ) : (
            <Low style={IconStyle.Outline} />
          )}
        </div>
      </div>
    </div>
  );
};

ProjectBox.defaultProps = {
  critical_vulnerabilities: 0,
  high_vulnerabilities: 0,
  medium_vulnerabilities: 0,
  low_vulnerabilities: 0,
};

export default ProjectBox;
