(this.webpackJsonpmars_photos_app_frontend=this.webpackJsonpmars_photos_app_frontend||[]).push([[0],{21:function(e,t,a){},42:function(e,t,a){"use strict";a.r(t);var n=a(1),r=a(16),c=a.n(r),s=(a(21),a(3)),o=a.n(s),l=a(7),i=a(4),u=a(0);var d=function(e){var t=e.date,a=e.updateDate,n=e.mostRecentDate;return Object(u.jsxs)("div",{className:"flex justify-between",children:[Object(u.jsx)("h1",{className:"text-4xl font-bold cursor-pointer",onClick:function(){return window.location.reload()},children:"Rovr"}),Object(u.jsxs)("form",{action:"",className:"text-2xl font-bold",onSubmit:function(e){e.preventDefault();var t=e.target[0].value.match(/(\d+)/g);if(3===t.length)if(0!==t[0]&&0!==t[1]&&0!==t[2]){var r=new Date(t[0],t[1]-1,t[2]),c=Date.parse("2021-06-01"),s=Date.parse(n);if(r<c||r>s)console.log("The database did not store pictures for that date. The earliest date for which there is data is '2021-06-01', and the latest is "+n);else{var o=r.getFullYear(),l=("0"+(r.getMonth()+1).toString()).slice(-2),i=("0"+r.getDate().toString()).slice(-2);a("".concat(o,"-").concat(l,"-").concat(i))}}else console.log("The inputted date was not formatted correctly");else console.log("The inputted date was not formatted correctly")},children:["Date: ",Object(u.jsx)("input",{type:"text",className:"font-bold",defaultValue:t})]})]})};var f=function(e){for(var t=e.updateCategory,a=e.picData,n=e.chosenCategory,r=Object.keys(a),c=0;c<Object.keys(a).length-4;)r[c].includes("_")?(r.push(r[c]),r.splice(c,1)):c++;return Object(u.jsx)("div",{className:"flex flex-col mt-10 text-lg",children:r.map((function(e,a){var r="";e===n&&(r="sidebar");var c=e;if(e.includes("_")){for(var s=e.split("_"),o=0;o<s.length;o++)s[o]=s[o][0].toUpperCase()+s[o].substr(1);s.includes("Month")&&s.splice(2,0,"of the"),c=s.join(" ")}return Object(u.jsx)("p",{className:"mt-10 cursor-pointer "+r,onClick:function(){return t(e)},children:c},a)}))})};var p=function(e){var t=e.pictureData,a=e.category,n=void 0;return n=a in t?t[a]:t.MAST_top20_overall,Object(u.jsx)("div",{className:"w-full ml-10 pt-5 flex items-center justify-center flex-wrap",children:n.map((function(e,t){return Object(u.jsxs)("div",{className:"flex flex-col imgContainer",children:[Object(u.jsx)("a",{href:"string"===typeof e?e:e.url,children:Object(u.jsx)("img",{className:"pl-3 pt-3",src:"string"===typeof e?e:e.url,alt:"",width:"200",height:"200"})}),e.date&&Object(u.jsxs)("p",{children:["Date: ",e.date]}),e.score&&Object(u.jsxs)("p",{children:["Score: ",JSON.stringify(e.score).substring(0,5)]})]},t)}))})};var j=function(e){var t=e.updateCategory,a=e.picData;return Object(u.jsxs)("div",{className:"flex p-10 justify-between fixed left-0 bottom-0 w-screen h-10",children:[Object(u.jsx)("p",{className:"text-xl font-bold cursor-pointer",onClick:function(){return t(Object.keys(a)[0])},children:"Home"}),Object(u.jsx)("p",{className:"text-xl font-bold cursor-pointer",onClick:function(){return window.location.reload()},children:"Refresh"})]})},h=a(5),b=a.n(h);var x=function(){var e=Object(n.useState)(null),t=Object(i.a)(e,2),a=t[0],r=t[1],c=Object(n.useState)(null),s=Object(i.a)(c,2),h=s[0],x=s[1],m=Object(n.useState)(null),O=Object(i.a)(m,2),v=O[0],g=O[1],y=Object(n.useState)(""),w=Object(i.a)(y,2),_=w[0],N=w[1],D=function(e){x(e)};return Object(n.useEffect)((function(){(function(){var e=Object(l.a)(o.a.mark((function e(){var t,a;return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,b.a.get("https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos");case 2:return t=e.sent,e.next=5,b.a.post("https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos",{earth_date:t.data});case 5:a=e.sent,r(a.data),x("MAST_top20_overall"),N(t.data),g(t.data);case 10:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}})()()}),[]),Object(n.useEffect)((function(){(function(){var e=Object(l.a)(o.a.mark((function e(){var t;return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,b.a.post("https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos",{earth_date:_});case 2:t=e.sent,r(t.data);case 4:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}})()()}),[_]),Object(u.jsx)("div",{className:"bg-yellow-100 min-h-screen flex flex-col font-mono",children:Object(u.jsxs)("div",{className:"flex flex-col p-10",children:[Object(u.jsx)(d,{updateDate:function(e){N(e)},date:_,recentDate:v}),Object(u.jsx)("div",{className:"flex",children:null!==a&&null!==h?Object(u.jsxs)(u.Fragment,{children:[Object(u.jsx)(f,{updateCategory:D,picData:a,chosenCategory:h}),Object(u.jsx)(p,{pictureData:a,category:h}),Object(u.jsx)(j,{updateCategory:D,picData:a})]}):Object(u.jsx)("div",{className:"loader-div",children:Object(u.jsx)("div",{className:"loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64"})})})]})})};var m=function(){return Object(u.jsx)(x,{})};c.a.render(Object(u.jsx)(m,{}),document.getElementById("root"))}},[[42,1,2]]]);
//# sourceMappingURL=main.0c3a398b.chunk.js.map