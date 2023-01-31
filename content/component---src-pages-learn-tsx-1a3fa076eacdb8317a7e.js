"use strict";(self.webpackChunk_freecodecamp_client=self.webpackChunk_freecodecamp_client||[]).push([[8013],{77587:function(e,t,n){var l=n(27378),a=n(39365),r=n(33570),c=n(52066),o=n(65240),i=c.forumLocation;function m(){var e=(0,a.$)().t;return l.createElement("div",{className:"intro-description"},l.createElement("strong",null,e("learn.read-this.heading")),l.createElement(o.LZ,null),l.createElement("p",null,e("learn.read-this.p1")),l.createElement("p",null,e("learn.read-this.p2")),l.createElement("p",null,e("learn.read-this.p3")),l.createElement("p",null,e("learn.read-this.p4")),l.createElement("p",null,e("learn.read-this.p5")),l.createElement("p",null,e("learn.read-this.p6")),l.createElement("p",null,e("learn.read-this.p7")),l.createElement("p",null,e("learn.read-this.p8")),l.createElement("p",null,l.createElement(r.c,{i18nKey:"learn.read-this.p9"},l.createElement(o.rU,{className:"inline",to:"https://youtube.com/freecodecamp"}))),l.createElement("p",null,e("learn.read-this.p10")),l.createElement("p",null,l.createElement(r.c,{i18nKey:"learn.read-this.p11"},l.createElement(o.rU,{className:"inline",to:i}))),l.createElement("p",null,e("learn.read-this.p12")))}m.displayName="IntroDescription",t.Z=m},40616:function(e,t,n){var l=n(25414);t.Z=function(e){return void 0===e&&(e="/"),function(){return"undefined"!=typeof window&&(0,l.navigate)(e),null}}},91794:function(e,t,n){var l=n(27378),a=n(47326),r=n(8736),c=n(81897),o=n(65240),i=n(69111),m=n(33309),u=n(9442),s=n(40616),d=(0,c.P1)(m.nl,m.Qi,m.np,(function(e,t,n){return{fetchState:e,isSignedIn:t,user:n}})),E={tryToShowDonationModal:i.dz},p=(0,s.Z)("/email-sign-up");t.Z=(0,r.$j)(d,E)((function(e){var t=e.isSignedIn,n=e.fetchState,r=e.user,c=e.tryToShowDonationModal,i=e.children;return(0,l.useEffect)((function(){c()}),[]),(0,l.useEffect)((function(){return function(){var e=document.querySelector('meta[name="robots"]');e&&e.remove()}}),[]),n.pending&&!n.complete?l.createElement(o.aN,{fullScreen:!0}):t&&!r.acceptedPrivacyTerms?l.createElement(p,null):l.createElement(l.Fragment,null,l.createElement(a.q,null,l.createElement("meta",{content:"noindex",name:"robots"})),l.createElement("main",{id:"learn-app-wrapper"},i),l.createElement(u.Z,null))}))},17374:function(e,t,n){n.r(t),n.d(t,{default:function(){return U}});var l=n(54404),a=n.n(l),r=n(82200),c=n.n(r),o=n(77529),i=n.n(o),m=n(27378),u=n(47326),s=n(39365),d=n(8736),E=n(81897),p=n(33140),f=n(33570),g=n(47810),h=n(55617),v=n(65240),b=n(77587),y=n(95764),S=n.n(y),N=n(59367),Z=function(e){var t=e.onDonationAlertClick,n=e.isDonating,l=(0,s.$)().t,a=(0,N.SS)("show-research-recruitment-alert"),r=(0,N.SS)("university-creation-alert"),c=(0,N.SS)("seasonal-alert"),o=m.createElement(S(),null,m.createElement("p",null,m.createElement("b",null,"Launching Oct 19"),": freeCodeCamp is teaming up with researchers from Stanford and UPenn to study how to help people build strong coding habits."),m.createElement("p",{style:{marginBottom:20,marginTop:14}},"Would you like to get involved? You’ll get free coaching from our scientists."),m.createElement("div",{style:{display:"flex",justifyContent:"center"}},m.createElement(v.rU,{className:"btn",key:"donate",sameTab:!1,to:"https://wharton.qualtrics.com/jfe/form/SV_57rJfXROkQDDU2y"},"Learn about HabitLab"))),i=m.createElement(S(),{bsStyle:"info",className:"annual-donation-alert"},m.createElement("p",null,m.createElement("b",null,l("learn.season-greetings-fcc"))),m.createElement("p",null,l("learn.if-getting-value")),m.createElement("hr",null),m.createElement("p",{className:"text-center"},m.createElement(v.rU,{className:"btn",key:"donate",sameTab:!1,to:"/donate",onClick:t},l("buttons.donate")))),u=m.createElement(S(),{bsStyle:"info",className:"annual-donation-alert"},m.createElement("p",null,m.createElement("b",null,l("learn.building-a-university"))),m.createElement("p",null,l("learn.if-help-university")),m.createElement("hr",null),m.createElement("p",{className:"text-center"},m.createElement(v.rU,{className:"btn",key:"donate",sameTab:!1,to:"/donate",onClick:t},l("donate.become-supporter"))));return a.on?o:r.on&&!n?u:c.on?i:null};Z.displayName="LearnAlert";var k=Z,C=function(e){var t=e.isSignedIn,n=e.name,l=e.pending,a=e.complete,r=e.completedChallengeCount,c=e.slug,o=e.onDonationAlertClick,i=e.isDonating,u=(0,s.$)().t;if(l&&!a)return m.createElement(m.Fragment,null,m.createElement(v.LZ,null),m.createElement(v.aN,null),m.createElement(v.LZ,null));if(t){var d=(0,g.C)(),E=d.quote,p=d.author;return m.createElement(m.Fragment,null,m.createElement(v.LZ,null),m.createElement("h1",{className:"text-center"},n?""+u("learn.welcome-1",{name:n}):""+u("learn.welcome-2")),m.createElement(v.LZ,null),m.createElement("div",{className:"text-center quote-partial"},m.createElement("blockquote",{className:"blockquote"},m.createElement("span",null,m.createElement("q",null,E),m.createElement("footer",{className:"quote-author blockquote-footer"},m.createElement("cite",null,p))))),m.createElement(k,{onDonationAlertClick:o,isDonating:i}),r&&c&&r<15?m.createElement("div",{className:"intro-description"},m.createElement(v.LZ,null),m.createElement("p",null,m.createElement(f.c,{i18nKey:"learn.start-at-beginning"},m.createElement(v.rU,{to:c})))):"")}return m.createElement(m.Fragment,null,m.createElement(v.LZ,null),m.createElement("h1",null,u("learn.heading")),m.createElement(v.LZ,null),m.createElement(b.Z,null),m.createElement(v.LZ,null),m.createElement(h.Z,{block:!0},u("buttons.logged-out-cta-btn")),m.createElement(v.LZ,null))};C.displayName="Intro";var L=C,D=n(17671),w=n(91794),q=n(43420),x=n(33309),A=n(69111),I=(0,E.P1)(x.nl,x.Qi,x.np,(function(e,t,n){return{fetchState:e,isSignedIn:t,user:n}}));function T(e){var t=e.isSignedIn,n=e.executeGA,l=e.fetchState,r=l.pending,o=l.complete,d=e.user,E=d.name,p=void 0===E?"":E,f=d.completedChallengeCount,g=void 0===f?0:f,h=d.isDonating,b=void 0!==h&&h,y=e.data.challengeNode.challenge.fields.slug,S=(0,s.$)().t;return m.createElement(w.Z,null,m.createElement(u.Z,{title:S("metaTags:title")}),m.createElement(a(),null,m.createElement(c(),null,m.createElement(i(),{md:8,mdOffset:2,sm:10,smOffset:1,xs:12},m.createElement(L,{complete:o,completedChallengeCount:g,isSignedIn:t,name:p,pending:r,slug:y,onDonationAlertClick:function(){n({event:"donationrelated",action:"Learn Donation Alert Click",duration:q.M4.donationDuration,amount:q.M4.donationAmount})},isDonating:b}),m.createElement(D.Z,null),m.createElement(v.LZ,{size:2})))))}T.displayName="LearnPage";var U=(0,d.$j)(I,(function(e){return(0,p.DE)({executeGA:A.pQ},e)}))(T)}}]);
//# sourceMappingURL=component---src-pages-learn-tsx-1a3fa076eacdb8317a7e.js.map