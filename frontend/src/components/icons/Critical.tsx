import { IconStyle } from "@/components/ProjectBox";

const outlineIcon = (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className="h-6 w-6 text-steel-blue"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
    strokeWidth={2}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016zM12 9v2m0 4h.01"
    />
  </svg>
);

const solidIcon = (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className="h-6 w-6 text-steel-blue"
    viewBox="0 0 20 20"
    fill="currentColor"
  >
    <path
      fillRule="evenodd"
      d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z"
      clipRule="evenodd"
    />
  </svg>
);

type ComponentProps = {
  style: IconStyle;
};

export default function Critical(props: ComponentProps) {
  return props.style === IconStyle.Outline ? outlineIcon : solidIcon;
}
