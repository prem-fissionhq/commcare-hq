hqDefine('app_manager/js/manage_releases', [
    'jquery',
    'knockout',
    'underscore',
    'hqwebapp/js/initial_page_data',
    'hqwebapp/js/widgets_v4',
], function (
    $,
    ko,
    _,
    initialPageData
) {
    'use strict';
    $(function () {
        var enabledAppRelease = function (details) {
            var self = {};
            self.id = details.id;
            self.build_id = details.build_id;
            self.active = ko.observable(details.active);
            self.app = details.app;
            self.version = details.version;
            self.location = details.location;
            self.activatedOn = ko.observable(details.activated_on);
            self.deactivatedOn = ko.observable(details.deactivated_on);
            self.errorMessage = ko.observable();
            self.dom_id = "restriction_" + self.id;
            self.ajaxInProgress = ko.observable(false);
            self.actionText = ko.computed(function () {
                return (self.active() ? "Remove" : "Add");
            });
            self.rowBgColor = ko.computed(function () {
                return (self.active() ? "lightblue" : "lightgrey");
            });
            self.toggleStatus = function () {
                self.active(!self.active());
            };
            self.error = ko.observable();
            self.requestUrl = function () {
                if (self.active()) {
                    return initialPageData.reverse('deactivate_release_restriction', self.id);
                }
                return initialPageData.reverse('activate_release_restriction', self.id);
            };
            self.toggleRestriction = function () {
                self.ajaxInProgress(true);
                var oldStatus = self.active();
                $.ajax({
                    method: 'POST',
                    url: self.requestUrl(),
                    success: function (data) {
                        if (data.success) {
                            self.toggleStatus();
                            self.activatedOn(data.activated_on);
                            self.deactivatedOn(data.deactivated_on);
                            self.error(false);
                        } else {
                            self.active(oldStatus);
                            self.errorMessage(data.message);
                        }
                    },
                    error: function () {
                        self.active(oldStatus);
                    },
                    complete: function () {
                        self.ajaxInProgress(false);
                        if (self.active() === oldStatus) {
                            self.error(true);
                        }
                    },
                });
            };
            return self;
        };

        function manageReleasesViewModel(enabledAppReleases) {
            var self = {};
            self.enabledAppReleases = ko.observableArray(enabledAppReleases);
            return self;
        }
        var enabledAppReleases = _.map(initialPageData.get('enabled_app_releases'), function (appRelease) {
            return enabledAppRelease(appRelease);
        });
        var viewModel = manageReleasesViewModel(enabledAppReleases);
        if (enabledAppReleases.length) {
            $('#managed_releases').koApplyBindings(viewModel);
        }
        function manageReleaseSearchViewModel() {
            var self = {};
            self.search = function () {
                var appId = $("#app_id_search_select").val();
                var locationId = $("#location_search_select").val();
                var version = $("#version_input").val();
                window.location.search = ("location_id=" + locationId + "&app_id=" + appId + "&version=" +
                    version);
            };
            self.clear = function () {
                window.location.search = "";
            };
            return self;
        }
        var searchViewModel = manageReleaseSearchViewModel();
        $("#manage_app_releases").koApplyBindings(searchViewModel);
    });
});