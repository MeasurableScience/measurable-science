/* eslint-disable */
(function () {
    /* eslint-disable */
    if (!window.$mcSite) {
        $mcSite = {
            optinFeatures: [],

            loadingPrerequisites: [],
            permissionProviders: {},

            registerPermissionProvider: function (permission, permissionResolutionPromise) {
                window.$mcSite.permissionProviders[permission] = permissionResolutionPromise;
            },

            enableOptIn: function () {
                this.createCookie("mc_user_optin", true, 365);
                this.optinFeatures.forEach(function (fn) {
                    fn();
                });
            },

            runIfOptedIn: function (fn, additionalPermissions) {
                Promise.all(this.loadingPrerequisites).then(function () {
                    this._runIfOptedIn.call(this, fn, additionalPermissions);
                }.bind(this));
            },

            _runIfOptedIn: function (fn, additionalPermissions) {
                if (!additionalPermissions || additionalPermissions.length === 0) {
                    if (this.hasOptedIn()) {
                        fn();
                    } else {
                        this.optinFeatures.push(fn);
                    }
                } else {
                    var wrappedPermmissionsFn = function () {
                        if (additionalPermissions.length === 0) {
                            fn();
                        }

                        // Get available permission providers
                        var permissionProviders = additionalPermissions.reduce(function (providers, permission) {
                            if (window.$mcSite.permissionProviders[permission]) {
                                providers.push(window.$mcSite.permissionProviders[permission]);
                            }
                            return providers;
                        }, []);

                        // Check if all permissions are granted
                        Promise.all(permissionProviders).then(function (results) {
                            var allPermissionsGranted = results.every(function (result) {
                                return result === true;
                            });

                            if (allPermissionsGranted) {
                                fn();
                            }
                        });
                    }

                    if (this.hasOptedIn()) {
                        wrappedPermmissionsFn();
                    } else {
                        this.optinFeatures.push(wrappedPermmissionsFn);
                    }
                }
            },

            hasOptedIn: function () {
                var cookieValue = this.readCookie("mc_user_optin");

                if (cookieValue === undefined) {
                    return true;
                }

                return cookieValue === "true";
            },

            createCookie: function (name, value, expirationDays) {
                var cookie_value = encodeURIComponent(value) + ";";

                if (expirationDays === undefined) {
                    throw new Error("expirationDays is not defined");
                }

                // set expiration
                if (expirationDays !== null) {
                    var expirationDate = new Date();
                    expirationDate.setDate(expirationDate.getDate() + expirationDays);
                    cookie_value += " expires=" + expirationDate.toUTCString() + ";";
                }

                cookie_value += "path=/";
                document.cookie = name + "=" + cookie_value;
            },

            readCookie: function (name) {
                var nameEQ = name + "=";
                var ca = document.cookie.split(";");

                for (var i = 0; i < ca.length; i++) {
                    var c = ca[i];

                    while (c.charAt(0) === " ") {
                        c = c.substring(1, c.length);
                    }

                    if (c.indexOf(nameEQ) === 0) {
                        return c.substring(nameEQ.length, c.length);
                    }
                }

                return undefined;
            }
        };
    }

    /* eslint-disable */
(function () {
    var availablePermissionResolvers = {
        'preferencesProcessingAllowed': function () {
            return new Promise(function (resolve) {
                try {
                    var result = window.Shopify.customerPrivacy.preferencesProcessingAllowed();
                    if (!result) {
                        throw new Error('Preferences processing not allowed');
                    }

                    resolve(result);
                } catch (e) {
                    document.addEventListener('visitorConsentCollected', function (event) {
                        if (event.detail && event.detail.preferencesAllowed) {
                            resolve(event.detail.preferencesAllowed);
                        }
                    });
                }
            })
        },

        'analyticsProcessingAllowed': function () {
            return new Promise(function (resolve) {
                try {
                    var result = window.Shopify.customerPrivacy.analyticsProcessingAllowed();

                    if (!result) {
                        throw new Error('Preferences processing not allowed');
                    }

                    resolve(result);
                } catch (e) {
                    document.addEventListener('visitorConsentCollected', function (event) {
                        if (event.detail && event.detail.analyticsAllowed) {
                            resolve(event.detail.analyticsAllowed);
                        }
                    });
                }

            })
        },
        'marketingAllowed': function () {
            return new Promise(function (resolve) {
                try {
                    var result = window.Shopify.customerPrivacy.marketingAllowed();

                    if (!result) {
                        throw new Error('Preferences processing not allowed');
                    }

                    resolve(result);
                } catch (e) {
                    document.addEventListener('visitorConsentCollected', function (event) {
                        if (event.detail && event.detail.marketingAllowed) {
                            resolve(event.detail.marketingAllowed);
                        }
                    });
                }
            })
        }
    };

    /* eslint-disable */
    if (window.$mcSite) {
        if (window.Shopify) {
            window.$mcSite.loadingPrerequisites.push(new Promise(function (resolve) {
                try {
                    window.Shopify.loadFeatures([
                        {
                            name: 'consent-tracking-api',
                            version: '0.1',
                        },
                    ],
                        function () {
                            if (window.Shopify.customerPrivacy) {

                                // Register the permission providers
                                var availablePermissions = Object.keys(availablePermissionResolvers);
                                for (var i = 0; i < availablePermissions.length; i++) {
                                    var permission = availablePermissions[i];

                                    window.$mcSite.registerPermissionProvider(permission, availablePermissionResolvers[permission]());
                                }
                            }
                            resolve();
                        }
                    );
                } catch (e) {
                    resolve();
                }
            }));
        }
    }
})();


    $mcSite.popup_form={settings:{base_url:"mc.us19.list-manage.com",list_id:"b7135a5f34",uuid:"0bb3fbb8bb53b930c6d91a811",skip_install:""}};
})();
(function () {
    if (window.$mcSite === undefined || window.$mcSite.popup_form === undefined) {
        return;
    }

    if (window.location.href.indexOf("checkout.shopify") >= 0) {
        return;
    }

    var scripts = document.getElementsByTagName("script");
    for (var i = 0; i < scripts.length; i++) {
        // look for src containing the old embed.js code and bail if it exists
        if (scripts[i].getAttribute("src") === "//s3.amazonaws.com/downloads.mailchimp.com/js/signup-forms/popup/embed.js" || scripts[i].getAttribute("src") === "//downloads.mailchimp.com/js/signup-forms/popup/embed.js") {
            return;
        }
    }

    var module = window.$mcSite.popup_form;

    if (module.installed === true) {
        return;
    }

    if (!module.settings) {
        return;
    }

    var settings = module.settings;

    if (!settings.base_url || !settings.uuid || !settings.list_id || settings.skip_install === "1") {
        return;
    }

    var script = document.createElement("script");

    script.src = "//downloads.mailchimp.com/js/signup-forms/popup/unique-methods/embed.js";
    script.type = "text/javascript";
    script.onload = function () {
        if (window.dojoRequire) {
            window.dojoRequire(["mojo/signup-forms/Loader"], function (L) { L.start({"baseUrl": settings.base_url, "uuid": settings.uuid, "lid": settings.list_id, "uniqueMethods": true}); });
        }
    };

    document.body.appendChild(script);

    window.$mcSite.popup_form.installed = true;
}());
