


(function(definition){ if(typeof define=="function"){define(definition);}else if(typeof YUI=="function"){YUI.add("es5-sham",definition);}else{definition();}})(function(){
if(!Object.getPrototypeOf){
 Object.getPrototypeOf=function getPrototypeOf(object){return object.__proto__||(object.constructor?object.constructor.prototype:prototypeOfObject);};}

if(!Object.getOwnPropertyDescriptor){var ERR_NON_OBJECT="Object.getOwnPropertyDescriptor called on a non-object: ";Object.getOwnPropertyDescriptor=function getOwnPropertyDescriptor(object,property){if((typeof object!="object"&&typeof object!="function")||object===null){throw new TypeError(ERR_NON_OBJECT+object);}
if(!owns(object,property)){return;}

var descriptor={enumerable:true,configurable:true};
if(supportsAccessors){



var prototype=object.__proto__;object.__proto__=prototypeOfObject;var getter=lookupGetter(object,property);var setter=lookupSetter(object,property);object.__proto__=prototype;if(getter||setter){if(getter){descriptor.get=getter;}
if(setter){descriptor.set=setter;}

return descriptor;}}

descriptor.value=object[property];return descriptor;};}

if(!Object.getOwnPropertyNames){Object.getOwnPropertyNames=function getOwnPropertyNames(object){return Object.keys(object);};}

if(!Object.create){Object.create=function create(prototype,properties){var object;if(prototype===null){object={"__proto__":null};}else{if(typeof prototype!="object"){throw new TypeError("typeof prototype["+(typeof prototype)+"] != 'object'");}
var Type=function(){};Type.prototype=prototype;object=new Type();

object.__proto__=prototype;}
if(properties!==void 0){Object.defineProperties(object,properties);}
return object;};}






function doesDefinePropertyWork(object){try{Object.defineProperty(object,"sentinel",{});return"sentinel"in object;}catch(exception){}}
if(Object.defineProperty){var definePropertyWorksOnObject=doesDefinePropertyWork({});var definePropertyWorksOnDom=typeof document=="undefined"||doesDefinePropertyWork(document.createElement("div"));if(!definePropertyWorksOnObject||!definePropertyWorksOnDom){var definePropertyFallback=Object.defineProperty;}}
if(!Object.defineProperty||definePropertyFallback){var ERR_NON_OBJECT_DESCRIPTOR="Property description must be an object: ";var ERR_NON_OBJECT_TARGET="Object.defineProperty called on non-object: "
var ERR_ACCESSORS_NOT_SUPPORTED="getters & setters can not be defined "+"on this javascript engine";Object.defineProperty=function defineProperty(object,property,descriptor){if((typeof object!="object"&&typeof object!="function")||object===null){throw new TypeError(ERR_NON_OBJECT_TARGET+object);}
if((typeof descriptor!="object"&&typeof descriptor!="function")||descriptor===null){throw new TypeError(ERR_NON_OBJECT_DESCRIPTOR+descriptor);}

if(definePropertyFallback){try{return definePropertyFallback.call(Object,object,property,descriptor);}catch(exception){}}
if(owns(descriptor,"value")){if(supportsAccessors&&(lookupGetter(object,property)||lookupSetter(object,property)))
{


var prototype=object.__proto__;object.__proto__=prototypeOfObject;
delete object[property];object[property]=descriptor.value;object.__proto__=prototype;}else{object[property]=descriptor.value;}}else{if(!supportsAccessors){throw new TypeError(ERR_ACCESSORS_NOT_SUPPORTED);}
if(owns(descriptor,"get")){defineGetter(object,property,descriptor.get);}
if(owns(descriptor,"set")){defineSetter(object,property,descriptor.set);}}
return object;};}

if(!Object.defineProperties){Object.defineProperties=function defineProperties(object,properties){for(var property in properties){if(owns(properties,property)&&property!="__proto__"){Object.defineProperty(object,property,properties[property]);}}
return object;};}

if(!Object.seal){Object.seal=function seal(object){

return object;};}

if(!Object.freeze){Object.freeze=function freeze(object){

return object;};}
try{Object.freeze(function(){});}catch(exception){Object.freeze=(function freeze(freezeObject){return function freeze(object){if(typeof object=="function"){return object;}else{return freezeObject(object);}};})(Object.freeze);}

if(!Object.preventExtensions){Object.preventExtensions=function preventExtensions(object){

return object;};}

if(!Object.isSealed){Object.isSealed=function isSealed(object){return false;};}

if(!Object.isFrozen){Object.isFrozen=function isFrozen(object){return false;};}

if(!Object.isExtensible){Object.isExtensible=function isExtensible(object){if(Object(object)!==object){throw new TypeError();}
var name='';while(owns(object,name)){name+='?';}
object[name]=true;var returnValue=owns(object,name);delete object[name];return returnValue;};}});

(function(definition){ if(typeof define=="function"){define(definition);}else if(typeof YUI=="function"){YUI.add("es5",definition);}else{definition();}})(function(){

if(!Function.prototype.bind){Function.prototype.bind=function bind(that){
var target=this;if(typeof target!="function"){throw new TypeError("Function.prototype.bind called on incompatible "+target);}
 
var args=slice.call(arguments,1);




var bound=function(){if(this instanceof bound){






var F=function(){};F.prototype=target.prototype;var self=new F;var result=target.apply(self,args.concat(slice.call(arguments)));if(Object(result)===result){return result;}
return self;}else{









return target.apply(that,args.concat(slice.call(arguments)));}};











return bound;};}


var call=Function.prototype.call;var prototypeOfArray=Array.prototype;var prototypeOfObject=Object.prototype;var slice=prototypeOfArray.slice;var _toString=call.bind(prototypeOfObject.toString);var owns=call.bind(prototypeOfObject.hasOwnProperty);var defineGetter;var defineSetter;var lookupGetter;var lookupSetter;var supportsAccessors;if((supportsAccessors=owns(prototypeOfObject,"__defineGetter__"))){defineGetter=call.bind(prototypeOfObject.__defineGetter__);defineSetter=call.bind(prototypeOfObject.__defineSetter__);lookupGetter=call.bind(prototypeOfObject.__lookupGetter__);lookupSetter=call.bind(prototypeOfObject.__lookupSetter__);}



if(!Array.isArray){Array.isArray=function isArray(obj){return _toString(obj)=="[object Array]";};}












if(!Array.prototype.forEach){Array.prototype.forEach=function forEach(fun){var self=toObject(this),thisp=arguments[1],i=-1,length=self.length>>>0; if(_toString(fun)!="[object Function]"){throw new TypeError();}
while(++i<length){if(i in self){ fun.call(thisp,self[i],i,self);}}};}


if(!Array.prototype.map){Array.prototype.map=function map(fun){var self=toObject(this),length=self.length>>>0,result=Array(length),thisp=arguments[1]; if(_toString(fun)!="[object Function]"){throw new TypeError(fun+" is not a function");}
for(var i=0;i<length;i++){if(i in self)
result[i]=fun.call(thisp,self[i],i,self);}
return result;};}


if(!Array.prototype.filter){Array.prototype.filter=function filter(fun){var self=toObject(this),length=self.length>>>0,result=[],value,thisp=arguments[1]; if(_toString(fun)!="[object Function]"){throw new TypeError(fun+" is not a function");}
for(var i=0;i<length;i++){if(i in self){value=self[i];if(fun.call(thisp,value,i,self)){result.push(value);}}}
return result;};}


if(!Array.prototype.every){Array.prototype.every=function every(fun){var self=toObject(this),length=self.length>>>0,thisp=arguments[1]; if(_toString(fun)!="[object Function]"){throw new TypeError(fun+" is not a function");}
for(var i=0;i<length;i++){if(i in self&&!fun.call(thisp,self[i],i,self)){return false;}}
return true;};}


if(!Array.prototype.some){Array.prototype.some=function some(fun){var self=toObject(this),length=self.length>>>0,thisp=arguments[1]; if(_toString(fun)!="[object Function]"){throw new TypeError(fun+" is not a function");}
for(var i=0;i<length;i++){if(i in self&&fun.call(thisp,self[i],i,self)){return true;}}
return false;};}


if(!Array.prototype.reduce){Array.prototype.reduce=function reduce(fun){var self=toObject(this),length=self.length>>>0; if(_toString(fun)!="[object Function]"){throw new TypeError(fun+" is not a function");} 
if(!length&&arguments.length==1){throw new TypeError('reduce of empty array with no initial value');}
var i=0;var result;if(arguments.length>=2){result=arguments[1];}else{do{if(i in self){result=self[i++];break;} 
if(++i>=length){throw new TypeError('reduce of empty array with no initial value');}}while(true);}
for(;i<length;i++){if(i in self){result=fun.call(void 0,result,self[i],i,self);}}
return result;};}


if(!Array.prototype.reduceRight){Array.prototype.reduceRight=function reduceRight(fun){var self=toObject(this),length=self.length>>>0; if(_toString(fun)!="[object Function]"){throw new TypeError(fun+" is not a function");} 
if(!length&&arguments.length==1){throw new TypeError('reduceRight of empty array with no initial value');}
var result,i=length-1;if(arguments.length>=2){result=arguments[1];}else{do{if(i in self){result=self[i--];break;} 
if(--i<0){throw new TypeError('reduceRight of empty array with no initial value');}}while(true);}
do{if(i in this){result=fun.call(void 0,result,self[i],i,self);}}while(i--);return result;};}


if(!Array.prototype.indexOf){Array.prototype.indexOf=function indexOf(sought){var self=toObject(this),length=self.length>>>0;if(!length){return-1;}
var i=0;if(arguments.length>1){i=toInteger(arguments[1]);} 
i=i>=0?i:Math.max(0,length+i);for(;i<length;i++){if(i in self&&self[i]===sought){return i;}}
return-1;};}


if(!Array.prototype.lastIndexOf){Array.prototype.lastIndexOf=function lastIndexOf(sought){var self=toObject(this),length=self.length>>>0;if(!length){return-1;}
var i=length-1;if(arguments.length>1){i=Math.min(i,toInteger(arguments[1]));} 
i=i>=0?i:length-Math.abs(i);for(;i>=0;i--){if(i in self&&sought===self[i]){return i;}}
return-1;};}


if(!Object.keys){ var hasDontEnumBug=true,dontEnums=["toString","toLocaleString","valueOf","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","constructor"],dontEnumsLength=dontEnums.length;for(var key in{"toString":null}){hasDontEnumBug=false;}
Object.keys=function keys(object){if((typeof object!="object"&&typeof object!="function")||object===null){throw new TypeError("Object.keys called on a non-object");}
var keys=[];for(var name in object){if(owns(object,name)){keys.push(name);}}
if(hasDontEnumBug){for(var i=0,ii=dontEnumsLength;i<ii;i++){var dontEnum=dontEnums[i];if(owns(object,dontEnum)){keys.push(dontEnum);}}}
return keys;};}






if(!Date.prototype.toISOString||(new Date(-62198755200000).toISOString().indexOf('-000001')===-1)){Date.prototype.toISOString=function toISOString(){var result,length,value,year;if(!isFinite(this)){throw new RangeError("Date.prototype.toISOString called on non-finite value.");}
result=[this.getUTCMonth()+1,this.getUTCDate(),this.getUTCHours(),this.getUTCMinutes(),this.getUTCSeconds()];year=this.getUTCFullYear();year=(year<0?'-':(year>9999?'+':''))+('00000'+Math.abs(year)).slice(0<=year&&year<=9999?-4:-6);length=result.length;while(length--){value=result[length];if(value<10){result[length]="0"+value;}}
return year+"-"+result.slice(0,2).join("-")+"T"+result.slice(2).join(":")+"."+
("000"+this.getUTCMilliseconds()).slice(-3)+"Z";}}

if(!Date.now){Date.now=function now(){return new Date().getTime();};}



if(!Date.prototype.toJSON){Date.prototype.toJSON=function toJSON(key){



if(typeof this.toISOString!="function"){throw new TypeError('toISOString property is not callable');}

return this.toISOString();



};}


if(!Date.parse||Date.parse("+275760-09-13T00:00:00.000Z")!==8.64e15){
Date=(function(NativeDate){ var Date=function Date(Y,M,D,h,m,s,ms){var length=arguments.length;if(this instanceof NativeDate){var date=length==1&&String(Y)===Y?
new NativeDate(Date.parse(Y)):
 length>=7?new NativeDate(Y,M,D,h,m,s,ms):length>=6?new NativeDate(Y,M,D,h,m,s):length>=5?new NativeDate(Y,M,D,h,m):length>=4?new NativeDate(Y,M,D,h):length>=3?new NativeDate(Y,M,D):length>=2?new NativeDate(Y,M):length>=1?new NativeDate(Y):new NativeDate(); date.constructor=Date;return date;}
return NativeDate.apply(this,arguments);};var isoDateExpression=new RegExp("^"+"(\\d{4}|[\+\-]\\d{6})"+"(?:-(\\d{2})"+"(?:-(\\d{2})"+"(?:"+"T(\\d{2})"+":(\\d{2})"+"(?:"+":(\\d{2})"+"(?:\\.(\\d{3}))?"+")?"+"(?:"+"Z|"+"(?:"+"([-+])"+"(\\d{2})"+":(\\d{2})"+")"+")?)?)?)?"+"$"); for(var key in NativeDate){Date[key]=NativeDate[key];} 
Date.now=NativeDate.now;Date.UTC=NativeDate.UTC;Date.prototype=NativeDate.prototype;Date.prototype.constructor=Date; Date.parse=function parse(string){var match=isoDateExpression.exec(string);if(match){match.shift();
 for(var i=1;i<7;i++){ match[i]=+(match[i]||(i<3?1:0));

if(i==1){match[i]--;}} 
var minuteOffset=+match.pop(),hourOffset=+match.pop(),sign=match.pop(); var offset=0;if(sign){ if(hourOffset>23||minuteOffset>59){return NaN;}

offset=(hourOffset*60+minuteOffset)*6e4*(sign=="+"?-1:1);}

 
var year=+match[0];if(0<=year&&year<=99){match[0]=year+400;return NativeDate.UTC.apply(this,match)+offset-12622780800000;} 
return NativeDate.UTC.apply(this,match)+offset;}
return NativeDate.parse.apply(this,arguments);};return Date;})(Date);}


var ws="\x09\x0A\x0B\x0C\x0D\x20\xA0\u1680\u180E\u2000\u2001\u2002\u2003"+"\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000\u2028"+"\u2029\uFEFF";if(!String.prototype.trim||ws.trim()){
ws="["+ws+"]";var trimBeginRegexp=new RegExp("^"+ws+ws+"*"),trimEndRegexp=new RegExp(ws+ws+"*$");String.prototype.trim=function trim(){if(this===undefined||this===null){throw new TypeError("can't convert "+this+" to object");}
return String(this).replace(trimBeginRegexp,"").replace(trimEndRegexp,"");};}



var toInteger=function(n){n=+n;if(n!==n){ n=0;}else if(n!==0&&n!==(1/0)&&n!==-(1/0)){n=(n>0||-1)*Math.floor(Math.abs(n));}
return n;};var prepareString="a"[0]!="a";
var toObject=function(o){if(o==null){ throw new TypeError("can't convert "+o+" to object");}
 
if(prepareString&&typeof o=="string"&&o){return o.split("");}
return Object(o);};});!function(a,b){function c(a,b){var c=a.createElement("p"),d=a.getElementsByTagName("head")[0]||a.documentElement;return c.innerHTML="x<style>"+b+"</style>",d.insertBefore(c.lastChild,d.firstChild)}function d(){var a=t.elements;return"string"==typeof a?a.split(" "):a}function e(a,b){var c=t.elements;"string"!=typeof c&&(c=c.join(" ")),"string"!=typeof a&&(a=a.join(" ")),t.elements=c+" "+a,j(b)}function f(a){var b=s[a[q]];return b||(b={},r++,a[q]=r,s[r]=b),b}function g(a,c,d){if(c||(c=b),l)return c.createElement(a);d||(d=f(c));var e;return e=d.cache[a]?d.cache[a].cloneNode():p.test(a)?(d.cache[a]=d.createElem(a)).cloneNode():d.createElem(a),!e.canHaveChildren||o.test(a)||e.tagUrn?e:d.frag.appendChild(e)}function h(a,c){if(a||(a=b),l)return a.createDocumentFragment();c=c||f(a);for(var e=c.frag.cloneNode(),g=0,h=d(),i=h.length;i>g;g++)e.createElement(h[g]);return e}function i(a,b){b.cache||(b.cache={},b.createElem=a.createElement,b.createFrag=a.createDocumentFragment,b.frag=b.createFrag()),a.createElement=function(c){return t.shivMethods?g(c,a,b):b.createElem(c)},a.createDocumentFragment=Function("h,f","return function(){var n=f.cloneNode(),c=n.createElement;h.shivMethods&&("+d().join().replace(/[\w\-:]+/g,function(a){return b.createElem(a),b.frag.createElement(a),'c("'+a+'")'})+");return n}")(t,b.frag)}function j(a){a||(a=b);var d=f(a);return!t.shivCSS||k||d.hasCSS||(d.hasCSS=!!c(a,"article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}mark{background:#FF0;color:#000}template{display:none}")),l||i(a,d),a}var k,l,m="3.7.2",n=a.html5||{},o=/^<|^(?:button|map|select|textarea|object|iframe|option|optgroup)$/i,p=/^(?:a|b|code|div|fieldset|h1|h2|h3|h4|h5|h6|i|label|li|ol|p|q|span|strong|style|table|tbody|td|th|tr|ul)$/i,q="_html5shiv",r=0,s={};!function(){try{var a=b.createElement("a");a.innerHTML="<xyz></xyz>",k="hidden"in a,l=1==a.childNodes.length||function(){b.createElement("a");var a=b.createDocumentFragment();return"undefined"==typeof a.cloneNode||"undefined"==typeof a.createDocumentFragment||"undefined"==typeof a.createElement}()}catch(c){k=!0,l=!0}}();var t={elements:n.elements||"abbr article aside audio bdi canvas data datalist details dialog figcaption figure footer header hgroup main mark meter nav output picture progress section summary template time video",version:m,shivCSS:n.shivCSS!==!1,supportsUnknownElements:l,shivMethods:n.shivMethods!==!1,type:"default",shivDocument:j,createElement:g,createDocumentFragment:h,addElements:e};a.html5=t,j(b)}(this,document);