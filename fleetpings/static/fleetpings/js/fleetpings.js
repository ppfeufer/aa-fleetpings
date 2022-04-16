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
    const selectFleetType = $('select#id_fleet_type');

    // Input fields
    const inputCsrfMiddlewareToken = $('input[name="csrfmiddlewaretoken"]');
    const inputFormupTime = $('input#id_formup_time');
    const inputFormupTimestamp = $('input#id_formup_timestamp');
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
     * Get the additional Discord ping targets for the current user
     */
    const getPingTargetsForCurrentUser = () => {
        $.ajax({
            url: fleetpingsSettings.url.pingTargets,
            success: (data) => {
                $('#id_ping_target').html(data);
            }
        });
    };

    /**
     * Get webhooks for current user
     */
    const getWebhooksForCurrentUser = () => {
        $.ajax({
            url: fleetpingsSettings.url.pingWebhooks,
            success: (data) => {
                $('#id_ping_channel').html(data);
            }
        });
    };

    /**
     * Get fleet types for current user
     */
    const getFleetTypesForCurrentUser = () => {
        $.ajax({
            url: fleetpingsSettings.url.fleetTypes,
            success: (data) => {
                $(selectFleetType).html(data);
            }
        });
    };

    /**
     * Get formup locations
     */
    const getFormupLocations = () => {
        $.ajax({
            url: fleetpingsSettings.url.formupLocations,
            success: (data) => {
                $('#id_formup_location').after(data);
            }
        });
    };

    /**
     * Get fleet comms
     */
    const getFleetComms = () => {
        $.ajax({
            url: fleetpingsSettings.url.fleetComms,
            success: (data) => {
                $('#id_fleet_comms').after(data);
            }
        });
    };

    /**
     * Get fleet doctrines for the current user
     */
    const getFleetDoctrines = () => {
        $.ajax({
            url: fleetpingsSettings.url.fleetDoctrines,
            success: (data) => {
                $('#id_fleet_doctrine').after(data);
            }
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
     * Show message when copy action was successful
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
     * Show message when copy action was not successful
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
        // Stop the browser from sending the form, we take care of it
        event.preventDefault();

        // Get the form data
        let formData = $('#aa-fleetping-form').serializeArray().reduce((obj, item) => {
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
                $('.aa-fleetpings-no-ping').hide('fast');
                $('.aa-fleetpings-ping').show('fast');

                $('.aa-fleetpings-ping-text').html(data);
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
     * Initialize functions that need to start on load
     */
    (() => {
        getPingTargetsForCurrentUser();
        getWebhooksForCurrentUser();
        getFleetTypesForCurrentUser();
        getFormupLocations();
        getFleetComms();
        getFleetDoctrines();
    })();
});
