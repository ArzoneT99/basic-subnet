(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[931],{7362:function(e,t,r){Promise.resolve().then(r.bind(r,7632))},7632:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return y}});var s=r(7437),n=r(2265),i=r(9143),a=r(7742),l=r(3167),o=r(1367);function d(){for(var e=arguments.length,t=Array(e),r=0;r<e;r++)t[r]=arguments[r];return(0,o.m6)((0,l.W)(t))}let c=(0,a.j)("inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",{variants:{variant:{default:"bg-primary text-primary-foreground hover:bg-primary/90",destructive:"bg-destructive text-destructive-foreground hover:bg-destructive/90",outline:"border border-input bg-background hover:bg-accent hover:text-accent-foreground",secondary:"bg-secondary text-secondary-foreground hover:bg-secondary/80",ghost:"hover:bg-accent hover:text-accent-foreground",link:"text-primary underline-offset-4 hover:underline"},size:{default:"h-10 px-4 py-2",sm:"h-9 rounded-md px-3",lg:"h-11 rounded-md px-8",icon:"h-10 w-10"}},defaultVariants:{variant:"default",size:"default"}}),u=n.forwardRef((e,t)=>{let{className:r,variant:n,size:a,asChild:l=!1,...o}=e,u=l?i.g7:"button";return(0,s.jsx)(u,{className:d(c({variant:n,size:a,className:r})),ref:t,...o})});u.displayName="Button";var f=r(4602);let m=(0,a.j)("text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"),h=n.forwardRef((e,t)=>{let{className:r,...n}=e;return(0,s.jsx)(f.f,{ref:t,className:d(m(),r),...n})});h.displayName=f.f.displayName;var p=r(5628),x=r(7019);let g=n.forwardRef((e,t)=>{let{className:r,...n}=e;return(0,s.jsx)(p.fC,{className:d("grid gap-2",r),...n,ref:t})});g.displayName=p.fC.displayName;let b=n.forwardRef((e,t)=>{let{className:r,...n}=e;return(0,s.jsx)(p.ck,{ref:t,className:d("aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",r),...n,children:(0,s.jsx)(p.z$,{className:"flex items-center justify-center",children:(0,s.jsx)(x.Z,{className:"h-2.5 w-2.5 fill-current text-current"})})})});async function v(){let e=await fetch("/api/questions",{cache:"no-store"});return(await e.json()).questions}function y(){var e;let[t,r]=(0,n.useState)(""),[i,a]=(0,n.useState)(null),[l,o]=(0,n.useState)([]);(0,n.useEffect)(()=>{v().then(e=>{o(e),e.length>0&&a(e[0].options?e[0].options[0]:"")})},[]);let d=async()=>{let e=await fetch("/api/answer",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:l[0].id,answer:i})});console.log(await e.json()),l.length>1?o(l.slice(1)):v().then(e=>{o(e)})};return 0===l.length?(0,s.jsxs)("div",{className:" h-screen flex flex-col items-center justify-center",children:[(0,s.jsx)("h1",{children:"No new questions..."}),(0,s.jsx)("p",{children:"Waiting for new questions please refresh the page after some time."})]}):(0,s.jsxs)("div",{className:"flex flex-col md:flex-row h-screen",children:[(0,s.jsxs)("div",{className:"md:w-1/2 md:p-4 flex flex-col items-center justify-center bg-yellow-200 p-8 overflow-y-scroll",children:[l[0].image&&(0,s.jsx)("img",{src:l[0].image,alt:"image associated with the question",className:"rounded-lg mb-4 w-full md:w-auto"}),(0,s.jsx)("p",{children:l[0].value})]}),(0,s.jsxs)("div",{className:"md:w-1/2 bg-white p-8 flex flex-col items-center md:items-start justify-center",children:[(0,s.jsx)("h2",{className:"text-xl font-bold mb-4 text-center md:text-left",children:l[0].label}),"select"===l[0].type?(0,s.jsx)(g,{defaultValue:l[0].options?l[0].options[0]:"",onValueChange:e=>{a(e)},children:null===(e=l[0].options)||void 0===e?void 0:e.map((e,t)=>(0,s.jsxs)("div",{className:"flex items-center space-x-2",children:[(0,s.jsx)(b,{value:e,id:e}),(0,s.jsx)(h,{htmlFor:e,children:e})]},t))}):(0,s.jsx)("input",{type:"text",value:t,onChange:e=>r(e.target.value),className:"border-2 border-gray-300 p-2 rounded-md"}),(0,s.jsx)("div",{className:"mt-4",children:(0,s.jsx)(u,{onClick:d,disabled:"select"===l[0].type&&null===i||"text"===l[0].type&&""===t,children:"Submit"})})]})]})}b.displayName=p.ck.displayName}},function(e){e.O(0,[529,971,69,744],function(){return e(e.s=7362)}),_N_E=e.O()}]);