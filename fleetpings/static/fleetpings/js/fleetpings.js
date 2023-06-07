/* global fleetpingsSettings, fleetpingsTranslations, ClipboardJS */

$(document).ready(() => {
    'use strict';

    /* Variables
    --------------------------------------------------------------------------------- */
    // Check boxes
    const checkboxPrePing = $('input#id_pre_ping');
    const checkboxFormupTimeNow = $('input#id_formup_now');
    const checkboxCreateSrpLink = $('input#id_srp_link');
    const checkboxCreateOptimer = $('input#id_optimer');
    const checkboxFleetSrp = $('input#id_srp');

    // Selects
    const selectPingTarget = $('select#id_ping_target');
    const selectPingChannel = $('select#id_ping_channel');
    const selectFleetType = $('select#id_fleet_type');

    // Input fields
    const inputCsrfMiddlewareToken = $('input[name="csrfmiddlewaretoken"]');
    const inputFleetCommander = $('input#id_fleet_commander');
    const inputFleetName = $('input#id_fleet_name');
    const inputFleetComms = $('input#id_fleet_comms');
    const inputFormupTime = $('input#id_formup_time');
    const inputFormupTimestamp = $('input#id_formup_timestamp');
    const inputFormupLocation = $('input#id_formup_location');
    const inputFleetDoctrine = $('input#id_fleet_doctrine');
    const inputFleetDoctrineUrl = $('input#id_fleet_doctrine_url');
    const inputWebhookEmbedColor = $('input#id_webhook_embed_color');

    // Initialize the datetime picker
    inputFormupTime.datetimepicker({
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
            const message = `An error has occurred: ${response.status}`;

            throw new Error(message);
        }

        return await response.text();
    };

    /**
     * Get the current user's dropdown data
     */
    const getUserDropdownData = () => {
        getDataFromAjaxUrl(fleetpingsSettings.url.pingTargets).then(pingTargets => {
            $(selectPingTarget).html(pingTargets);
        });
        getDataFromAjaxUrl(fleetpingsSettings.url.pingWebhooks).then(pingWebhooks => {
            $(selectPingChannel).html(pingWebhooks);
        });
        getDataFromAjaxUrl(fleetpingsSettings.url.fleetTypes).then(fleetTypes => {
            $(selectFleetType).html(fleetTypes);
        });
        getDataFromAjaxUrl(fleetpingsSettings.url.formupLocations).then(formupLocations => {
            $(inputFormupLocation).after(formupLocations);
        });
        getDataFromAjaxUrl(fleetpingsSettings.url.fleetComms).then(fleetComms => {
            $(inputFleetComms).after(fleetComms);
        });
        getDataFromAjaxUrl(fleetpingsSettings.url.fleetDoctrines).then(fleetDoctrines => {
            $(inputFleetDoctrine).after(fleetDoctrines);
        });
    };

    /**
     * Closing the message
     *
     * @param {string} element
     * @param {int} closeAfter Close Message after given time in seconds (Default: 10)
     */
    const closeMessageElement = (element, closeAfter = 10) => {
        $(element).fadeTo(closeAfter * 1000, 500).slideUp(500, () => {
            $(this).slideUp(500, () => {
                $(this).remove();
            });
        });
    };

    /**
     * Show a message when copy action was successful
     *
     * @param {string} message
     * @param {string} element
     */
    const showSuccess = (message, element) => {
        $(element).html(
            '<div class="alert alert-success alert-dismissable alert-message-success">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message +
            '</div>'
        );

        closeMessageElement('.alert-message-success');
    };

    /**
     * Show a message when copy action was not successful
     *
     * @param {string} message
     * @param {string} element
     */
    const showError = (message, element) => {
        $(element).html(
            '<div class="alert alert-danger alert-dismissable alert-message-error">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message +
            '</div>'
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
                /<(|\/|[^>\/bi]|\/[^>bi]|[^\/>][^>]+|\/[^>][^>]+)>/g,
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
                fleetpingsTranslations.copyToClipboard.success,
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
                fleetpingsTranslations.copyToClipboard.error,
                '.aa-fleetpings-ping-copyresult'
            );

            clipboardFleetPingData.destroy();
        });
    };

    /* Events
    --------------------------------------------------------------------------------- */
    /**
     * Show a hint about ping spam for `@everyone`
     */
    $(selectPingTarget).change(() => {
        if (selectPingTarget.val() === '@everyone') {
            $('.hint-ping-everyone').show('fast');
        } else {
            $('.hint-ping-everyone').hide('fast');
        }
    });

    /**
     * Set the formup timestamp when formup time is changed
     */
    $(inputFormupTime).change(() => {
        const formupTimestamp = getFormupTimestamp(
            sanitizeInput(inputFormupTime.val())
        );

        $(inputFormupTimestamp).val(formupTimestamp);
    });

    /**
     * Set the fleet doctrine URL if we have one
     */
    $(inputFleetDoctrine).change(() => {
        const fleetDoctrine = sanitizeInput(inputFleetDoctrine.val());
        let fleetDoctrineLink = null;

        if (fleetDoctrine !== '') {
            const selectedLink = $(
                '#fleetDoctrineList [value="' + escapeInput(fleetDoctrine, false) + '"]'
            ).data('doctrine-url');

            if ('undefined' !== selectedLink && selectedLink !== '') {
                // Houston, we have a link!
                fleetDoctrineLink = selectedLink;
            }
        }

        $(inputFleetDoctrineUrl).val(fleetDoctrineLink);
    });

    /**
     * Set the webhook embed color
     */
    $(selectFleetType).change(() => {
        const fleetTypeSelected = $('option:selected', selectFleetType);
        let webhookEmbedColor = null;

        if (fleetTypeSelected !== '') {
            webhookEmbedColor = sanitizeInput(fleetTypeSelected.data('embed-color'));
        }

        $(inputWebhookEmbedColor).val(webhookEmbedColor);
    });

    /**
     * Toggle "Create SRP Link" checkbox
     */
    if (fleetpingsSettings.srpModuleAvailableToUser === true) {
        if (checkboxFleetSrp.is(':checked') && checkboxFormupTimeNow.is(':checked')) {
            $('.fleetpings-create-srp-link').show('fast');
        } else {
            checkboxCreateSrpLink.prop('checked', false);
            $('.fleetpings-create-srp-link').hide('fast');
        }

        checkboxFleetSrp.change(() => {
            if (checkboxFleetSrp.is(':checked') && checkboxFormupTimeNow.is(':checked')) {
                $('.fleetpings-create-srp-link').show('fast');
            } else {
                checkboxCreateSrpLink.prop('checked', false);
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
     */
    checkboxPrePing.on('change', () => {
        if (checkboxPrePing.is(':checked')) {
            checkboxFormupTimeNow.prop('checked', false);
            inputFormupTime.prop('disabled', false);

            if (fleetpingsSettings.optimerInstalled === true) {
                $('.fleetpings-create-optimer').show('fast');
            }

            if (fleetpingsSettings.srpModuleAvailableToUser === true) {
                checkboxCreateSrpLink.prop('checked', false);
                $('.fleetpings-create-srp-link').hide('fast');
            }
        } else {
            checkboxFormupTimeNow.prop('checked', true);
            inputFormupTime.prop('disabled', true);

            if (fleetpingsSettings.optimerInstalled === true) {
                checkboxCreateOptimer.prop('checked', false);
                $('.fleetpings-create-optimer').hide('fast');
            }

            if (fleetpingsSettings.srpModuleAvailableToUser === true && checkboxFleetSrp.is(':checked')) {
                $('.fleetpings-create-srp-link').show('fast');
            }
        }
    });

    checkboxFormupTimeNow.on('change', () => {
        if (checkboxFormupTimeNow.is(':checked')) {
            checkboxPrePing.prop('checked', false);
            inputFormupTime.prop('disabled', true);

            if (fleetpingsSettings.optimerInstalled === true) {
                checkboxCreateOptimer.prop('checked', false);
                $('.fleetpings-create-optimer').hide('fast');
            }

            if (fleetpingsSettings.srpModuleAvailableToUser === true && checkboxFleetSrp.is(':checked')) {
                $('.fleetpings-create-srp-link').show('fast');
            }
        } else {
            checkboxPrePing.prop('checked', true);
            inputFormupTime.prop('disabled', false);

            if (fleetpingsSettings.optimerInstalled === true) {
                $('.fleetpings-create-optimer').show('fast');
            }

            if (fleetpingsSettings.srpModuleAvailableToUser === true) {
                checkboxCreateSrpLink.prop('checked', false);
                $('.fleetpings-create-srp-link').hide('fast');
            }
        }
    });

    /**
     * Generate ping text
     */
    $('form').submit((event) => {
        // Stop the browser from sending the form, we take care of it here …
        event.preventDefault();

        // Close all possible form messages
        $('.fleetpings-form-message div').remove();

        if (fleetpingsSettings.srpModuleAvailableToUser === true && checkboxCreateSrpLink.is(':checked')) {
            const srpMandatoryFields = [
                inputFleetName.val(),
                inputFleetDoctrine.val()
            ];

            // Check if all required fields for SRP links are filled
            if (srpMandatoryFields.includes('')) {
                showError(
                    fleetpingsTranslations.srp.error.missingFields,
                    '.fleetpings-form-message'
                );

                return false;
            }
        }

        if (fleetpingsSettings.optimerInstalled === true && checkboxCreateOptimer.is(':checked')) {
            const optimerMandatoryFields = [
                inputFleetName.val(),
                inputFleetDoctrine.val(),
                inputFormupLocation.val(),
                inputFormupTime.val(),
                inputFleetCommander.val()
            ];

            if (optimerMandatoryFields.includes('')) {
                showError(
                    fleetpingsTranslations.optimer.error.missingFields,
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
                'X-CSRFToken': inputCsrfMiddlewareToken.val()
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
     */
    $('button#copyFleetPing').on('click', () => {
        copyFleetPing();
    });

    /**
     * FlexDatalist
     * http://projects.sergiodinislopes.pt/flexdatalist/
     */
    $('.flexdatalist').flexdatalist({
        minLength: 1, noResultsText: '', searchContain: true
    });

    /**
     * Initialize functions that need to start on load
     */
    (() => {
        getUserDropdownData();
    })();
});
