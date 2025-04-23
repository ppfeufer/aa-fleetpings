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
     * Get data from a given ajax URL
     *
     * @param {string} url The URL to query
     * @returns {Promise<string>}
     */
    const getDataFromAjaxUrl = async (url) => {
        const response = await fetch(url);

        if (!response.ok) {
            const message = `Error ${response.status}: ${response.statusText}`;

            throw new Error(message);
        }

        return await response.text();
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
        getDataFromAjaxUrl(fleetpingsSettings.url.pingTargets).then((pingTargets) => {
            if (pingTargets !== '') {
                $(fleetpingsVars.selectPingTarget).html(pingTargets);
            }
        }).catch((error) => {
            console.error('Error fetching ping targets:', error);
        });

        // Webhooks
        getDataFromAjaxUrl(fleetpingsSettings.url.pingWebhooks).then((webhooks) => {
            if (webhooks !== '') {
                $(fleetpingsVars.selectPingChannel).html(webhooks);
            }
        }).catch((error) => {
            console.error('Error fetching webhooks:', error);
        });

        // Fleet types
        getDataFromAjaxUrl(fleetpingsSettings.url.fleetTypes).then((fleetTypes) => {
            if (fleetTypes !== '') {
                $(fleetpingsVars.selectFleetType).html(fleetTypes);
            }
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
        getDataFromAjaxUrl(fleetpingsSettings.url.formupLocations).then((formupLocations) => {
            if (formupLocations.trim() !== '') {
                $(fleetpingsVars.inputFormupLocation).after(formupLocations);

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
        getDataFromAjaxUrl(fleetpingsSettings.url.fleetComms).then((fleetComms) => {
            if (fleetComms.trim() !== '') {
                $(fleetpingsVars.inputFleetComms).after(fleetComms);

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
        getDataFromAjaxUrl(fleetpingsSettings.url.fleetDoctrines).then((fleetDoctrines) => {
            if (fleetDoctrines.trim() !== '') {
                $(fleetpingsVars.inputFleetDoctrine).after(fleetDoctrines);

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
            console.error('Error fetching fleet doctrines:', error);
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

        $.ajax({
            url: fleetpingsSettings.url.fleetPing,
            type: 'post',
            data: formData,
            headers: {
                'X-CSRFToken': fleetpingsVars.inputCsrfMiddlewareToken.val()
            },
            success: (data) => {
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
                } else {
                    if (data.message) {
                        showError(
                            data.message,
                            '.fleetpings-form-message'
                        );
                    } else {
                        showError(
                            'Something went wrong, no details given.',
                            '.fleetpings-form-message'
                        );
                    }
                }
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
