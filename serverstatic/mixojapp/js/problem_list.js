$(document).ready(function() {
    //跨域攻击防护
    //var csrftoken = $.cookie('csrftoken');
    //function csrfSafeMethod(method) {
    //    // these HTTP methods do not require CSRF protection
    //    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    //}
    //$.ajaxSetup({
    //    beforeSend: function(xhr, settings) {
    //        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
    //            xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //        }
    //    }
    //});

    var select_all_checkbox = $("#select_all");
    select_all_checkbox.click(function() {
        var select_status = select_all_checkbox.prop("checked");
        //alert(select_status);
        if (select_status == true) {
            $("input[name='problem-update-checkbox']").each(function() {
                var cur_checkbox = $(this);
                cur_checkbox.prop("checked", true);
            });
        } else if (select_status == false) {
            $("input[name='problem-update-checkbox']").each(function() {
                var cur_checkbox = $(this);
                cur_checkbox.prop("checked", false);
            });
        }
    });

    var update_button = $("#update-button");
    update_button.click(function() {
        var problem_id_need_update = [];
        var cnt = 0;
        $("input[name='problem-update-checkbox']:checked").each(function() {
            var cur_checkbox = $(this);
            problem_id_need_update[cnt++] = cur_checkbox.prop("id");
            //alert(cur_checkbox.prop("id"));
        });
        post_data = {
            problems: problem_id_need_update
        };
        $.post("/update_problems", post_data, function(data){
            if (data["res"] == "success") {
                window.location.reload();
                //alert("update success");
            } else {
                alert(data["msg"]);
            }
        }, 'json');
    });
});
