//// AdSage Tracking Analytics Crumb
//// Copyright 2008 AdSage, All Rights Reserved.

function _ataTracker()
{
	this.url="http://analytics.adsage.cn/atac.gif?";
	this.params={ver:"1.0"};

	this._history={};

	var doc=document;
	var loc=doc.location;
	
	var queries={
	"baidu":["wd","word","w"],
	"sogou":"query",
	"google":"q",
	"yahoo":"p",
	"msn":"q",
	"live":"q",
	"zhongsou":"w",
	"soso":"w",
	"beijixing":"query",
	"aol":["query","encquery","q"],
	"lycos":"query",
	"ask":"q",
	"cnn":"query",
	"about":"terms",
	"mamma":"query",
	"voila":"rdata",
	"alice":"qs",
	"yandex":"text",
	"najdi":"q",
	"mama":"query",
	"seznam":"q",
	"search":"q",
	"wp":"szukaj",
	"onet":"qt",
	"yam":"k",
	"pchome":"q",
	"kvasir":"searchExpr",
	"sesam":"q",
	"ozu":"q",
	"terra":"query",
	"mynet":"q",
	"ekolay":"q",
	"nostrum":"query",
	"altavista":"q",
	"netscape":"query",
	"looksmart":"qt",
	"alltheweb":"q",
	"gigablast":"q",
	"virgilio":"qs",
	"netsprint":"q",
	"szukacz":"q",
	"club-internet":"query",
	"google.interia":"q",
	"search.ilse":"search_for"
	};

	this.isLocal=loc.protocol=="file:";

	this.localEnabled=false;

	this.encoder=function(str)
	{
		if (typeof(encodeURIComponent) == 'function')
		{
			return encodeURIComponent(str);
		}
		else
		{
			return escape(str);
		}
	}

	this.parseRef=function()
	{
		var ref=doc.referrer;
		if (ref&&ref!="")
		{
			this.params["ref"]=ref;
			var url=ref;
			switch (loc.protocol)
			{
			case "file:":
			case "http:":
				url=ref.substring(7);
				break;
			case "https:":
				url=ref.substring(8);
				break;
			default:
				url="";
				break;
			}
			if (url!=""&&(doc.domain==""||url.indexOf(doc.domain)!=0))
			{
				var src=url;
				var query="";
				if (url.indexOf("/")>-1)
				{
					src=url.substring(0,url.indexOf("/"));
				}
				var getKey=function (key)
				{
					var pos=ref.indexOf("&"+key+"=");
					if (pos==-1) pos=ref.indexOf("?"+key+"=");
					if (pos>-1)
					{
						return ref.substring(pos+key.length+2).split("/")[0].split("#")[0].split("&")[0];
					}
					return "";
				}
				for (var source in queries)
				{
					if (src.indexOf(source)>-1)
					{
						var key=queries[source];
						if (typeof(key)=="string")
						{
							query=getKey(key);
						}
						else
						{
							for (var i=0; i<key.length; i++)
							{
								var q=getKey(key[i]);
								if (q!="")
								{
									var arr=q.split("+");
									query=arr.join(" ");
									break;
								}
							}
						}
					}
				}
				doc.cookie="__atasr="+src+"|"+query;
			}
		}
		else
		{
			doc.cookie="__atasr=(direct)";
		}
	}

	this.parseCookie=function()
	{
		if (doc.cookie&&doc.cookie!="")
		{
			var arr=doc.cookie.split(";");
			for (var i=0; i<arr.length; i++)
			{
				var crumb=arr[i].split("=");
				if (crumb[0]=="__atasr")
				{
					var srq=crumb[1].split("|");
					this.params["src"]=srq[0];
					if (srq[0]!="(direct)"&&srq[1]&&srq[1]!="")
					{
						this.params["q"]=srq[1];
					}
				}
			}
		}
	}

	this.parseClient=function()
	{
		var n=navigator;
		if (screen)
		{
			this.params["sr"]=screen.width+"x"+screen.height;
			this.params["sc"]=screen.colorDepth;
		}
		this.params["je"]=n.javaEnabled()?"1":"0";
		var f="";
		if (n.plugins && n.plugins.length)
		{
			for (var i=0;i<n.plugins.length;i++)
			{
				if (n.plugins[i].name.indexOf('Shockwave Flash')!=-1)
				{
					f=n.plugins[i].description.split('Shockwave Flash ')[1];
					break;
				}
			}
		}
		else
		{
			var fl;
			try
			{
				fl = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");
				f = fl.GetVariable("$version");
			} catch(e) {}
			if (f == "")
			{
				try
				{
					fl = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");
					f = "WIN 6,0,21,0";
					fl.AllowScriptAccess = "always";
					f = fl.GetVariable("$version");
				} catch(e) {}
			}
			if (f == "")
			{
				try
				{
					fl = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
					f = fl.GetVariable("$version");
				} catch(e) {}
			}
			if (f != "")
			{
				f = f.split(" ")[1].split(",");
				f = f[0] + "." + f[1] + " r" + f[2];
			}
		}
		if (f!="") this.params["fl"]=f;
	}

	this.parseDoc=function()
	{
		if (doc.characterSet) this.params["cs"]=doc.characterSet;
		else if (doc.charset) this.params["cs"]=doc.charset;
		if (doc.title&&doc.title!="") this.params["dt"]=doc.title;
	}

	this.parseRef();
	this.parseCookie();
	this.parseClient();
	this.parseDoc();
}

_ataTracker.prototype.setTags=function(tags)
{
	if (!tags||tags=="") return;
	var arr=tags.split("|");
	var result=[];
	for (var i=0; i<arr.length; i++)
	{
		var tag=arr[i];
		if (tag!="")
		{
			var hasTag=false;
			for (var j=0; j<result.length; j++)
			{
				if (result[j]==tag)
				{
					hasTag=true;
					break;
				}
			}
			if (!hasTag) result.push(tag);
		}
	}
	this.params["tag"]=result.join("|");
}

_ataTracker.prototype.setAccount=function(acc)
{
	if (!acc||acc=="") return;
	this.params["acc"]=acc;
}

_ataTracker.prototype.setConversion=function(cid,csid)
{
	if (!cid||!csid||cid==""||csid=="") return;
	this.params["cid"]=cid;
	this.params["csid"]=csid;
}

_ataTracker.prototype.addKey=function(key,val)
{
	if (!key||!val||key==""||val=="") return;
	this.params["_"+key]=val;
}

_ataTracker.prototype.track=function()
{
	if (!this.localEnabled&&this.isLocal) return;
	if (this.params["acc"]&&this.params["acc"]!="")
	{
		var arr=[];
		for (var key in this.params)
		{
			var val=this.params[key];
			if (val&&typeof(val)!="function"&&val!="") arr.push(key+"="+this.encoder(val));
		}
		var trc=this.url+arr.join("&");
		if (!this._history[trc])
		{
			this._history[trc]=true;
			var img=new Image(1,1);
			img.src=trc;
		}
	}
}

var ataTracker=new _ataTracker();