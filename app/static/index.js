function get_data() {
    return $.ajax({
        url: "./get-data", 
        method: "POST", 
        success: function(res) {
            return res;
        }
    });
}

function refresh_table() {
    get_data().then((res) => {
        var columns = [];
        for (c in res[0]) {
            columns.push({field: c, title: c, sortable: true});
        }
        $("#file-output table").bootstrapTable("refreshOptions", {
            data: res, 
            columns: columns
        });
    });
}

$(document).ready(function() {

    $.ajax({
        url: "./remove-prev-ids", 
        method: "POST"
    });

    $("#file-output table").bootstrapTable({
        pageSize: 5, 
        pagination: true
    });
    
    $("#content").hide()
    if (sessionStorage.getItem("uploaded")) {
        $("#content").show()
        refresh_table();
    }

    $("#upload-file").change(function() {

        var files = $(this).prop("files")[0];
        var data = new FormData();
        data.append("files", files);

        $.ajax({
            url: "./upload-data", 
            method: "POST", 
            processData: false, 
            contentType: false, 
            data: data, 
            success: function(res) {
                refresh_table();
                $("#content").show();
                sessionStorage.setItem("uploaded", true);
            }
        });
    });

    $("#add-btn").on("click", function() {
        $.ajax({
            url: "./create-config-html", 
            method: "POST", 
            data: {"n": $(".chart-group").length + 1}, 
            success: function(res) {
                $("#create-config-container").append(res["html"]);
            }
        });
    });

    $("#create-config-container").on("change", ".form-select[name='chart']", function() {
        var chart_group = $(this).closest(".chart-group");
        $.ajax({
            url: "./create-config-html", 
            method: "POST", 
            data: {"chart": $(this).val(), "n": $(this).closest(".chart-group").attr("data-num")}, 
            success: function(res) {
                chart_group.replaceWith(res["html"]);
            }
        });
        return false;
    });

    $("#create-config-container").on("click", ".generate-btn", function() {
        var form_grp = $(this).closest("form.chart-group");
        var plot_container = form_grp.find(".plot-container");
        console.log(plot_container);
        $.ajax({
            url: "./create-chart-html", 
            method: "POST", 
            data: form_grp.serialize(), 
            success: function(res) {
                plot_container.replaceWith(res);
                console.log(1);
            }
        });
        return false;
    });

    $("#create-config-container").on("click", ".remove-btn", function() {
        var this_form_grp = $(this).closest("form.chart-group");
        var prev_form_grps = this_form_grp.nextAll("form.chart-group");

        prev_form_grps.each(function() {
            var num = $(this).attr("data-num");
            var target = $(this).find(".accordion-button");
            var target_str = $(this).find(".accordion-button").attr("data-bs-target").replace(num, num-1);
            $(this).attr("data-num", num-1);
            $(target).attr("data-bs-target", target_str);
        })
        $(this_form_grp).remove();
        
        return false;
    });

    $("#generate-all-btn").click(function() {
        var data = [];
        $("form.chart-group").each(function() {
            data.push($(this).serialize());
        });

        $.ajax({
            url: "./generate-all", 
            method: "POST", 
            data: {
                "data": data, 
                "heading": $("#heading-config input[name='heading']").val(),
                "comment": $("#heading-config input[name='comment']").val(),
            }, 
            success: function(res) {
                console.log(typeof(res));
                let blob = new Blob([res]);
                let a = document.createElement("a");
                let url = window.URL.createObjectURL(blob);
                a.href = url;
                a.download = "output.html";
                a.click();
                window.URL.revokeObjectURL(url);
            }
        });
    })

});