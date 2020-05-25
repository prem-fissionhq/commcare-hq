/*
 *  TODO
 */
hqDefine('hqwebapp/js/activity', [
    'jquery',
    'underscore',
    'hqwebapp/js/initial_page_data',
], function (
    $,
    _,
    initialPageData
) {
    $(function () {
        var delay = 10 * 1000;
        var interval = setInterval(function () {
            $.ajax({
                url: initialPageData.reverse('cloudcare_ping'),
                type: 'GET',
                success: function (data) {
                    if (!data.success) {
                        clearInterval(interval);
                        var $modal = $("#inactivityModal");
                        var content = _.template('<iframe src="<%= src %>" height="<%= height %>" width="<%= width %>"></iframe>')({
                            // TODO: add ?next=
                            // TODO: instead of login, a new view that just tells them to click something to show they're active? in case they're not logged out yet?
                            // TODO: get rid of everything that makes login look like a full page
                            // TODO: what if user clicks on something undesireable? reset password worfklow?
                            src: initialPageData.reverse('login') + "?next=" + initialPageData.reverse('login_new_window'),
                            width: 700,     // TODO: account for screen size
                            height: 300,    // TODO: account for screen size
                        });
                        $modal.find(".modal-body").html(content);
                        $modal.modal('show');
                    } else {
                        console.log("success");
                    }
                },
            });
        }, delay);
    });

    return 1;
});
