$(function(){var a={opacity:0.6,handle:"h2",placeholder:"sort_helper",connectWith:".drop-area",items:".sort",scroll:true,tolerance:"pointer",start:function(c,b){b.placeholder.height(b.helper.height());b.placeholder.css("margin-bottom",b.helper.css("margin-bottom"))},change:function(d,c){var f=c.placeholder,b=c.item[0];if($(b).hasClass("vonly")&&this!==b.parentNode){f.html("此模块只能垂直拖动")}else{f.html("")}},stop:function(h,f){var d=f.item[0],j=d.id.toLowerCase(),b=d.parentNode,i=$(b).hasClass("aside")?"r":"l",g=[],c=[];if(this!==b){if($(d).hasClass("vonly")){$(this).sortable("cancel")}else{$.getJSON(mine_page_url+"?t="+j+"&pos="+i,function(e){$(d).replaceWith(e.html)})}}$(".article .sort").each(function(){var e=$(this).find("#extra")[0];g.push(e?this.id+e.value:this.id)});$(".aside .sort").each(function(){var e=$(this).find("#extra")[0];c.push(e?this.id+e.value:this.id)});$.post(mine_page_url,{layout:"l:"+g.join(",")+";r:"+c.join(","),ck:get_cookie("ck")})}};$(".article, .aside").addClass("drop-area").sortable(a)});