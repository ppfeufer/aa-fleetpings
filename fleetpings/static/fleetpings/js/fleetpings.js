/* global fleetpingsSettings, ClipboardJS */

import Autocomplete from '/static/fleetpings/libs/bootstrap5-autocomplete/1.1.39/autocomplete.min.js';

$(document).ready(() => {
    'use strict';

    /* Variables
    --------------------------------------------------------------------------------- */
    const fleetpingsVars= {
        // Check boxes
        checkboxPrePing: $('input#id_pre_ping'),
        checkboxFormupTimeNow: $('input#id_formup_now'),
        checkboxCreateSrpLink: $('input#id_srp_link'),
        checkboxCreateOptimer: $('input#id_optimer'),
        checkboxFleetSrp: $('input#id_srp'),

        // Selects
        selectPingTarget: $('select#id_ping_target'),
        selectPingChannel: $('select#id_ping_channel'),
        selectFleetType: $('select#id_fleet_type'),

        // Input fields
        inputCsrfMiddlewareToken: $('input[name="csrfmiddlewaretoken"]'),
        inputFleetComms: $('input#id_fleet_comms'),
        inputFleetCommander: $('input#id_fleet_commander'),
        inputFleetName: $('input#id_fleet_name'),
        inputFormupTime: $('input#id_formup_time'),
        inputFormupTimestamp: $('input#id_formup_timestamp'),
        inputFormupLocation: $('input#id_formup_location'),
        inputFleetDoctrine: $('input#id_fleet_doctrine'),
        inputFleetDoctrineUrl: $('input#id_fleet_doctrine_url'),
        inputWebhookEmbedColor: $('input#id_webhook_embed_color'),
    };

    // Initialize the datetime picker
    fleetpingsVars.inputFormupTime.datetimepicker({
        lang: fleetpingsSettings.dateTimeLocale,
        maskInput: true,
        format: 'Y-m-d H:i',
        dayOfWeekStart: 1,
        step: 15
    });

    /* Functions
    --------------------------------------------------------------------------------- */

    /**
     * Checks if the given item is a plain object, excluding arrays and dates.
     *
     * @param {*} item - The item to check.
     * @returns {boolean} True if the item is a plain object, false otherwise.
     */
    const isObject = (item) => {
        return (
            item && typeof item === 'object' && !Array.isArray(item) && !(item instanceof Date)
        );
    };

    /**
     * Fetch data from an ajax URL
     *
     * @param {string} url The URL to fetch data from
     * @param {string} method The HTTP method to use for the request (default: 'get')
     * @param {string|null} csrfToken The CSRF token to include in the request headers (default: null)
     * @param {string|null} payload The payload (JSON) to send with the request (default: null)
     * @param {boolean} responseIsJson Whether the response is expected to be JSON or not (default: true)
     * @returns {Promise<any>} The fetched data
     */
    const _fetchAjaxData = async ({
        url,
        method = 'get',
        csrfToken = null,
        payload = null,
        responseIsJson = true
    }) => {
        const normalizedMethod = method.toLowerCase();

        // Validate the method
        if (!['get', 'post'].includes(normalizedMethod)) {
            throw new Error(`Invalid method: ${method}. Valid methods are: get, post`);
        }

        const headers = {};

        // Set headers based on response type
        if (responseIsJson) {
            headers['Accept'] = 'application/json'; // jshint ignore:line
            headers['Content-Type'] = 'application/json';
        }

        let requestUrl = url;
        let body = null;

        if (normalizedMethod === 'post') {
            if (!csrfToken) {
                throw new Error('CSRF token is required for POST requests');
            }

            headers['X-CSRFToken'] = csrfToken;

            if (payload !== null && !isObject(payload)) {
                throw new Error('Payload must be an object when using POST method');
            }

            body = payload ? JSON.stringify(payload) : null;
        } else if (normalizedMethod === 'get' && payload) {
            const queryParams = new URLSearchParams(payload).toString(); // jshint ignore:line

            requestUrl += (url.includes('?') ? '&' : '?') + queryParams;
        }

        try {
            const response = await fetch(requestUrl, {
                method: method.toUpperCase(),
                headers: headers,
                body: body
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return responseIsJson ? await response.json() : await response.text();
        } catch (error) {
            console.log(`Error: ${error.message}`);

            throw error;
        }
    };

    /**
     * Fetch data from an ajax URL using the GET method.
     * This function is a wrapper around _fetchAjaxData to simplify GET requests.
     *
     * @param {string} url The URL to fetch data from
     * @param {string|null} payload The payload (JSON) to send with the request (default: null)
     * @param {boolean} responseIsJson Whether the response is expected to be JSON or not (default: true)
     */
    const fetchGet = ({
        url,
        payload = null,
        responseIsJson = true
    }) => {
        return _fetchAjaxData({
            url: url,
            method: 'get',
            payload: payload,
            responseIsJson: responseIsJson
        });
    };

    /**
     * Fetch data from an ajax URL using the POST method.
     * This function is a wrapper around _fetchAjaxData to simplify POST requests.
     * It requires a CSRF token for security purposes.
     *
     * @param {string} url The URL to fetch data from
     * @param {string|null} csrfToken The CSRF token to include in the request headers (default: null)
     * @param {string|null} payload The payload (JSON) to send with the request (default: null)
     * @param {boolean} responseIsJson Whether the response is expected to be JSON or not (default: true)
     */
    const fetchPost = ({
        url,
        csrfToken,
        payload = null,
        responseIsJson = true
    }) => {
        return _fetchAjaxData({
            url: url,
            method: 'post',
            csrfToken: csrfToken,
            payload: payload,
            responseIsJson: responseIsJson
        });
    };


    /**
     * Get user dropdown data from the server for the selects
     *
     * These are the ping targets, ping webhooks, and fleet types.
     *
     * @returns {void}
     */
    const getUserDropdownDataForSelects = () => {
        // Ping targets
        fetchGet({url: fleetpingsSettings.url.pingTargets, responseIsJson: false})
            .then((data) => {
                $(fleetpingsVars.selectPingTarget).html(data);
            }).catch((error) => {
                console.error('Error fetching ping targets:', error);
            });

        // Webhooks
        fetchGet({url: fleetpingsSettings.url.pingWebhooks, responseIsJson: false})
            .then((data) => {
                $(fleetpingsVars.selectPingChannel).html(data);
            }).catch((error) => {
                console.error('Error fetching webhooks:', error);
            });

        // Fleet types
        fetchGet({url: fleetpingsSettings.url.fleetTypes, responseIsJson: false})
            .then((data) => {
                $(fleetpingsVars.selectFleetType).html(data);
            }).catch((error) => {
                console.error('Error fetching fleet types:', error);
            });
    };

    /**
     * Get user dropdown data from the server for the data lists
     *
     * These are the formup locations, fleet comms, and fleet doctrines,
     * and the data lists will be converted to autocomplete fields.
     *
     * @returns {void}
     */
    const getUserDropdownDataForDatalist = () => {
        const opts = {
            onSelectItem: (selected_item, datalist) => {
                if (datalist.e.datalist === 'fleet-doctrine-list') {
                    setFleetDoctrineUrl();
                }
            },
            preventBrowserAutocomplete: true,
        };

        // Formup locations
        fetchGet({url: fleetpingsSettings.url.formupLocations, responseIsJson: false})
            .then((data) => {
                if (data.trim() !== '') {
                    $(fleetpingsVars.inputFormupLocation).after(data);

                    const optsFormupLocation = Object.assign(
                        {},
                        opts,
                        {
                            onRenderItem: (item, label) => {
                                return `<l-i set="fl" name="${item.value.toLowerCase()}" size="16"></l-i> ${label}`;
                            },
                        }
                    );

                    const autoCompleteFleetComms = new Autocomplete( // eslint-disable-line no-unused-vars
                        document.getElementById('id_formup_location'),
                        optsFormupLocation
                    );
                }
            }).catch((error) => {
                console.error('Error fetching formup locations:', error);
            });

        // Fleet comms
        fetchGet({url: fleetpingsSettings.url.fleetComms, responseIsJson: false})
            .then((data) => {
                if (data.trim() !== '') {
                    $(fleetpingsVars.inputFleetComms).after(data);

                    const optsFleetComms = Object.assign(
                        {},
                        opts,
                        {
                            onRenderItem: (item, label) => {
                                return `<l-i set="fl" name="${item.value.toLowerCase()}" size="16"></l-i> ${label}`;
                            },
                        }
                    );

                    const autoCompleteFleetComms = new Autocomplete( // eslint-disable-line no-unused-vars
                        document.getElementById('id_fleet_comms'),
                        optsFleetComms
                    );
                }
            }).catch((error) => {
                console.error('Error fetching fleet comms:', error);
            });

        // Fleet doctrines
        fetchGet({url: fleetpingsSettings.url.fleetDoctrines, responseIsJson: false})
            .then((data) => {
                if (data.trim() !== '') {
                    $(fleetpingsVars.inputFleetDoctrine).after(data);

                    const optsFleetDoctrine = Object.assign(
                        {},
                        opts,
                        {
                            onRenderItem: (item, label) => {
                                return `<l-i set="fl" name="${item.value.toLowerCase()}" size="16"></l-i> ${label}`;
                            },
                        }
                    );

                    const autoCompleteFleetComms = new Autocomplete( // eslint-disable-line no-unused-vars
                        document.getElementById('id_fleet_doctrine'),
                        optsFleetDoctrine
                    );
                }
            }).catch((error) => {
                console.error('Error fetching fleet comms:', error);
            });
    };

    /**
     * Closing the message
     *
     * @param {string} element
     * @param {int} closeAfter Close Message after given time in seconds (Default: 10)
     * @returns {void}
     */
    const closeMessageElement = (element, closeAfter = 10) => {
        $(element).fadeTo(closeAfter * 1000, 500).slideUp(500, () => {
            $(element).remove();
        });
    };

    /**
     * Show a success message box
     *
     * @param {string} message
     * @param {string} element
     * @returns {void}
     */
    const showSuccess = (message, element) => {
        $(element).html(
            `<div class="alert alert-success alert-dismissible alert-message-success d-flex align-items-center fade show">${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`
        );

        closeMessageElement('.alert-message-success');
    };

    /**
     * Show an error message box
     *
     * @param {string} message
     * @param {string} element
     * @returns {void}
     */
    const showError = (message, element) => {
        $(element).html(
            `<div class="alert alert-danger alert-dismissible alert-message-error d-flex align-items-center fade show">${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`
        );

        closeMessageElement('.alert-message-error', 9999);
    };

    /**
     * Sanitize input string
     *
     * @param {string} input String to sanitize
     * @returns {string} Sanitized string
     */
    const sanitizeInput = (input) => {
        if (input) {
            return input.replace(
                /<(|\/|[^>/bi]|\/[^>bi]|[^/>][^>]+|\/[^>][^>]+)>/g,
                ''
            );
        } else {
            return input;
        }
    };

    /**
     * Escape input string
     *
     * @param {string} input String to escape
     * @param {boolean} quotesToEntities Transform quotes into entities
     * @returns {string} Escaped string
     */
    const escapeInput = (input, quotesToEntities) => {
        quotesToEntities = quotesToEntities || false;

        if (input) {
            let returnValue = sanitizeInput(input).replace(
                /&/g,
                '&amp;'
            );

            if (quotesToEntities === true) {
                returnValue = returnValue.replace(
                    /"/g,
                    '&quot;'
                );
            }

            if (quotesToEntities === false) {
                returnValue = returnValue.replace(
                    /"/g,
                    '\\"'
                );
            }

            return returnValue;
        } else {
            return input;
        }
    };

    /**
     * Get the timestamp for the formup time
     *
     * @param {string} formupTime
     * @returns {number}
     */
    const getFormupTimestamp = (formupTime) => {
        const formupDateTime = new Date(formupTime);

        return (formupDateTime.getTime() - formupDateTime.getTimezoneOffset() * 60 * 1000) / 1000;
    };

    /**
     * Copy the fleet ping to clipboard
     *
     * @returns {void}
     */
    const copyFleetPing = () => {
        /**
         * Copy text to clipboard
         *
         * @type Clipboard
         */
        const clipboardFleetPingData = new ClipboardJS('button#copyFleetPing');

        /**
         * Copy success
         *
         * @param {type} e
         */
        clipboardFleetPingData.on('success', (e) => {
            showSuccess(
                fleetpingsSettings.translation.copyToClipboard.success,
                '.aa-fleetpings-ping-copyresult'
            );

            e.clearSelection();
            clipboardFleetPingData.destroy();
        });

        /**
         * Copy error
         */
        clipboardFleetPingData.on('error', () => {
            showError(
                fleetpingsSettings.translation.copyToClipboard.error,
                '.aa-fleetpings-ping-copyresult'
            );

            clipboardFleetPingData.destroy();
        });
    };

    /* Events
    --------------------------------------------------------------------------------- */
    /**
     * Show a hint about ping spam for `@everyone`
     *
     * @returns {void}
     */
    $(fleetpingsVars.selectPingTarget).change(() => {
        if (fleetpingsVars.selectPingTarget.val() === '@everyone') {
            $('.hint-ping-everyone').show('fast');
        } else {
            $('.hint-ping-everyone').hide('fast');
        }
    });

    /**
     * Set the formup timestamp when formup time is changed
     *
     * @returns {void}
     */
    $(fleetpingsVars.inputFormupTime).change(() => {
        const formupTimestamp = getFormupTimestamp(
            sanitizeInput(fleetpingsVars.inputFormupTime.val())
        );

        $(fleetpingsVars.inputFormupTimestamp).val(formupTimestamp);
    });

    /**
     * Set the fleet doctrine URL if we have one
     *
     * @returns {void}
     */
    const setFleetDoctrineUrl = () => {
        const fleetDoctrine = sanitizeInput(fleetpingsVars.inputFleetDoctrine.val());
        let fleetDoctrineLink = null;

        if (fleetDoctrine !== '') {
            const selectedLink = $(
                '#fleet-doctrine-list [value="' + escapeInput(fleetDoctrine, false) + '"]'
            ).data('doctrine-url');

            if ('undefined' !== selectedLink && selectedLink !== '') {
                // Houston, we have a link!
                fleetDoctrineLink = selectedLink;
            }
        }

        $(fleetpingsVars.inputFleetDoctrineUrl).val(fleetDoctrineLink);
    };

    /**
     * Set the webhook embed color
     *
     * @returns {void}
     */
    $(fleetpingsVars.selectFleetType).change(() => {
        const fleetTypeSelected = $('option:selected', fleetpingsVars.selectFleetType);
        let webhookEmbedColor = null;

        if (fleetTypeSelected !== '') {
            webhookEmbedColor = sanitizeInput(fleetTypeSelected.data('embed-color'));
        }

        $(fleetpingsVars.inputWebhookEmbedColor).val(webhookEmbedColor);
    });

    /**
     * Toggle "Create SRP Link" checkbox
     */
    if (fleetpingsSettings.srpModuleAvailableToUser === true) {
        if (fleetpingsVars.checkboxFleetSrp.is(':checked') && fleetpingsVars.checkboxFormupTimeNow.is(':checked')) {
            $('.fleetpings-create-srp-link').show('fast');
        } else {
            fleetpingsVars.checkboxCreateSrpLink.prop('checked', false);
            $('.fleetpings-create-srp-link').hide('fast');
        }

        fleetpingsVars.checkboxFleetSrp.change(() => {
            if (fleetpingsVars.checkboxFleetSrp.is(':checked') && fleetpingsVars.checkboxFormupTimeNow.is(':checked')) {
                $('.fleetpings-create-srp-link').show('fast');
            } else {
                fleetpingsVars.checkboxCreateSrpLink.prop('checked', false);
                $('.fleetpings-create-srp-link').hide('fast');
            }
        });
    }

    /**
     * Toggle "Formup NOW" checkbox when "Pre-Ping" is toggled
     *
     * Behaviour:
     *  Pre-Ping checked
     *      » Formup NOW unchecked
     *      » Create Optimer is unchecked and hidden
     *      » Create SRP Link is displayed
     *  Pre-Ping unchecked
     *      » Formup NOW checked
     *      » Create Optimer is displayed
     *      » Create SRP Link is hidden and unchecked
     *
     * @returns {void}
     */
    fleetpingsVars.checkboxPrePing.on('change', () => {
        if (fleetpingsVars.checkboxPrePing.is(':checked')) {
            fleetpingsVars.checkboxFormupTimeNow.prop('checked', false);
            fleetpingsVars.inputFormupTime.prop('disabled', false);

            if (fleetpingsSettings.optimerInstalled === true) {
                $('.fleetpings-create-optimer').show('fast');
            }

            if (fleetpingsSettings.srpModuleAvailableToUser === true) {
                fleetpingsVars.checkboxCreateSrpLink.prop('checked', false);
                $('.fleetpings-create-srp-link').hide('fast');
            }
        } else {
            fleetpingsVars.checkboxFormupTimeNow.prop('checked', true);
            fleetpingsVars.inputFormupTime.prop('disabled', true);

            if (fleetpingsSettings.optimerInstalled === true) {
                fleetpingsVars.checkboxCreateOptimer.prop('checked', false);
                $('.fleetpings-create-optimer').hide('fast');
            }

            if (fleetpingsSettings.srpModuleAvailableToUser === true && fleetpingsVars.checkboxFleetSrp.is(':checked')) {
                $('.fleetpings-create-srp-link').show('fast');
            }
        }
    });

    fleetpingsVars.checkboxFormupTimeNow.on('change', () => {
        if (fleetpingsVars.checkboxFormupTimeNow.is(':checked')) {
            fleetpingsVars.checkboxPrePing.prop('checked', false);
            fleetpingsVars.inputFormupTime.prop('disabled', true);

            if (fleetpingsSettings.optimerInstalled === true) {
                fleetpingsVars.checkboxCreateOptimer.prop('checked', false);
                $('.fleetpings-create-optimer').hide('fast');
            }

            if (fleetpingsSettings.srpModuleAvailableToUser === true && fleetpingsVars.checkboxFleetSrp.is(':checked')) {
                $('.fleetpings-create-srp-link').show('fast');
            }
        } else {
            fleetpingsVars.checkboxPrePing.prop('checked', true);
            fleetpingsVars.inputFormupTime.prop('disabled', false);

            if (fleetpingsSettings.optimerInstalled === true) {
                $('.fleetpings-create-optimer').show('fast');
            }

            if (fleetpingsSettings.srpModuleAvailableToUser === true) {
                fleetpingsVars.checkboxCreateSrpLink.prop('checked', false);
                $('.fleetpings-create-srp-link').hide('fast');
            }
        }
    });

    /**
     * Generate ping text
     *
     * @returns {void}
     */
    $('form').submit((event) => {
        // Stop the browser from sending the form, we take care of it here …
        event.preventDefault();

        // Close all possible form messages
        $('.fleetpings-form-message div').remove();

        if (fleetpingsSettings.srpModuleAvailableToUser === true && fleetpingsVars.checkboxCreateSrpLink.is(':checked')) {
            const srpMandatoryFields = [
                fleetpingsVars.inputFleetName.val(),
                fleetpingsVars.inputFleetDoctrine.val()
            ];

            // Check if all required fields for SRP links are filled
            if (srpMandatoryFields.includes('')) {
                showError(
                    fleetpingsSettings.translation.srp.error.missingFields,
                    '.fleetpings-form-message'
                );

                return false;
            }
        }

        if (fleetpingsSettings.optimerInstalled === true && fleetpingsVars.checkboxCreateOptimer.is(':checked')) {
            const optimerMandatoryFields = [
                fleetpingsVars.inputFleetName.val(),
                fleetpingsVars.inputFleetDoctrine.val(),
                fleetpingsVars.inputFormupLocation.val(),
                fleetpingsVars.inputFormupTime.val(),
                fleetpingsVars.inputFleetCommander.val()
            ];

            if (optimerMandatoryFields.includes('')) {
                showError(
                    fleetpingsSettings.translation.optimer.error.missingFields,
                    '.fleetpings-form-message'
                );

                return false;
            }
        }

        // Get the form data
        const formData = $('#aa-fleetping-form').serializeArray().reduce((obj, item) => {
            obj[item.name] = item.value;

            return obj;
        }, {});

        fetchPost({
            url: fleetpingsSettings.url.fleetPing,
            csrfToken: fleetpingsVars.inputCsrfMiddlewareToken.val(),
            payload: formData,
            responseIsJson: true
        }).then((data) => {
            if (data.success === true) {
                $('.aa-fleetpings-no-ping').hide('fast');
                $('.aa-fleetpings-ping').show('fast');

                $('.aa-fleetpings-ping-text').html(data.ping_context);

                if (data.message) {
                    showSuccess(
                        data.message,
                        '.fleetpings-form-message'
                    );
                }
            }
        }).catch((error) => {
            console.error(`Error: ${error.message}`);

            if (error.message) {
                showError(
                    error.message,
                    '.fleetpings-form-message'
                );
            } else {
                showError(
                    'Something went wrong, no details given.',
                    '.fleetpings-form-message'
                );
            }
        });
    });

    /**
     * Copy ping text
     *
     * @returns {void}
     */
    $('button#copyFleetPing').on('click', () => {
        copyFleetPing();
    });

    /**
     * Initialize functions that need to start on load
     */
    (() => {
        getUserDropdownDataForSelects();
        getUserDropdownDataForDatalist();
    })();
});
