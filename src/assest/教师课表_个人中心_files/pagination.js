(function($) {
  var zp = {
    init: function(obj, pageinit) {
      return (function() {
        zp.addhtml(obj, pageinit);
        zp.bindEvent(obj, pageinit);
      })();
    },
    addhtml: function(obj, pageinit) {
      return (function() {
        obj.empty();
		obj.append(
		  "<span>" +
            pageinit.pagehtml+
		    "</span>"
		);
		obj.append(
		  "<span>" +
			"<font style='color:#272727;'>" +
            pageinit.pagehtml1+
			"</font>" +
		    "</span>"
		);
		obj.append(
		  "<p style='width:100px;margin-right:8px;display:inline-block;line-height:32px;'>" +
            pageinit.pagehtml2+
		  "</p>"
		);
        if (pageinit.current > 1) {
		  obj.append('<a href="javascript:;" class="btnbox"><i class="layui-icon layui-icon-prev prebtn"></i><i class="layui-icon layui-icon-left prebtns"></i></a>');
        } else {
          obj.remove(".prevPage");
		  obj.append('<span class="disabled"><i class="layui-icon layui-icon-prev"></i><i class="layui-icon layui-icon-left"></i></span>');
        }
        // if (pageinit.current > 3 && pageinit.pageNum > 3) {
        //   obj.append('<a href="javascript:;" class="pageNumber">' + 1 + "</a>");
        //   obj.append("<span>...</span>");
        // }
        if (pageinit.current > 3 && pageinit.current <= pageinit.pageNum - 4) {
          var start = pageinit.current - 1,
            end = pageinit.current + 1;
        } else if (
          pageinit.current > 3 &&
          pageinit.current > pageinit.pageNum - 4
        ) {
          var start = pageinit.pageNum - 4,
            end = pageinit.pageNum;
        } else {
          var start = 1,
            end = 4;
        }
        // for (; start <= end; start++) {
        //   if (start <= pageinit.pageNum && start >= 1) {
        //     if (start == pageinit.current) {
        //       obj.append('<span class="current">' + start + "</span>");
        //     } else if (start == pageinit.current + 1) {
        //       obj.append(
        //         '<a href="javascript:;" class="pageNumber nextpage">' +
        //           start +
        //           "</a>"
        //       );
        //     } else {
        //       obj.append(
        //         '<a href="javascript:;" class="pageNumber">' + start + "</a>"
        //       );
        //     }
        //   }
        // }
        // if (end < pageinit.pageNum) {
        //   obj.append("<span>...</span>");
        //   obj.append('<a href="javascript:;" class="pageNumber">' + pageinit.pageNum + "</a>");
        // }

		// obj.append('<span class="current">' + pageinit.current + "</span>");
		obj.append('<input class="current" id="curPage"/>');
		$('#curPage').val(pageinit.current);
        if (pageinit.current >= pageinit.pageNum) {
          obj.remove(".nextbtn");
          obj.append('<span class="disabled"><i class="layui-icon layui-icon-right"></i><i class="layui-icon layui-icon-next"></i></span>');
        } else {
          obj.append('<a href="javascript:;" class="btnbox"><i class="layui-icon layui-icon-right nextbtn"></i><i class="layui-icon layui-icon-next nextbtns"></i></a>');
        }
        // obj.append(
        //   "<span>" +
        //     "到第" +
        //     '<input type="number" class="paginationInput" value=""/>' +
        //     "页" +
        //     "</span>"
        // );
        // obj.append('<span class="confirmBtn">' + "确定" + "</span>");
      })();
    },
    bindEvent: function(obj, pageinit) {
      return (function() {
        obj.on("click", "a .prebtn", function() {
          var cur = parseInt(obj.children("input.current").val());
          var current = $.extend(pageinit, { current: 1 });
          zp.addhtml(obj, current);
          if (typeof pageinit.backfun == "function") {
            pageinit.backfun(current);
          }
        });
		obj.on("click", "a .prebtns", function() {
		  var cur = parseInt(obj.children("input.current").val());
		  var current = $.extend(pageinit, { current: cur - 1 });
		  zp.addhtml(obj, current);
		  if (typeof pageinit.backfun == "function") {
		    pageinit.backfun(current);
		  }
		});
        // obj.on("click", "a.pageNumber", function() {
        //   var cur = parseInt($(this).text());
        //   var current = $.extend(pageinit, { current: cur });
        //   zp.addhtml(obj, current);
        //   if (typeof pageinit.backfun == "function") {
        //     pageinit.backfun(current);
        //   }
        // });
        obj.on("click", "a .nextbtn", function() {
          var cur = parseInt(obj.children("input.current").val());
          var current = $.extend(pageinit, { current: cur + 1 });
          zp.addhtml(obj, current);
          if (typeof pageinit.backfun == "function") {
            pageinit.backfun(current);
          }
        });
		obj.on("click", "a .nextbtns", function() {
		  var cur = parseInt(obj.children("input.current").val());
		  var current = $.extend(pageinit, { current: pageinit.pageNum });
		  zp.addhtml(obj, current);
		  if (typeof pageinit.backfun == "function") {
		    pageinit.backfun(current);
		  }
		});
        // obj.on("click", "span.confirmBtn", function() {
        //   var cur = parseInt($("input.paginationInput").val());
        //   var current = $.extend(pageinit, { current: cur });
        //   zp.addhtml(obj, { current: cur, pageNum: pageinit.pageNum });
        //   if (typeof pageinit.backfun == "function") {
        //     pageinit.backfun(current);
        //   }
        // });
		$('#curPage').bind('keydown', function(event) {
			 if (event.keyCode == "13") {
                 // alert('转到' + $('#curPage').val() + '页');
                 var pageSize = $("#tablePagination_rowsPerPage").val();
                 reloadPageOnFy($('#curPage').val() ,pageSize);
			}
		});
      })();
    }
  };
  $.fn.createPage = function(options) {
    var pageinit = $.extend(
      { pageNum: 15, current: 1, total:1000, each:10,userlanguage:0, backfun: function() {} },
      options
    );
    zp.init(this, pageinit);
  };
})(jQuery);
