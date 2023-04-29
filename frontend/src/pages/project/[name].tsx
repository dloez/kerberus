import { useRouter } from "next/router";
import { useEffect } from "react";

function Project() {
  const router = useRouter();
  const { name } = router.query;

  useEffect(() => {
    console.log(name);
  });

  return (
    <div className="w-full h-full">
      <aside className="w-64 h-full bg-dark-navy-blue border-l-[1px] border-steel-blue absolute"></aside>
    </div>
  );
}

export default Project;
