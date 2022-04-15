/* global fleetpingsSettings, fleetpingsTranslations, ClipboardJS, console */

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
    // const selectPingTarget = $('select#id_ping_target');
    // const selectPingChannel = $('select#id_ping_channel');
    // const selectFleetType = $('select#id_fleet_type');

    // Input fields
    const inputCsrfMiddlewareToken = $('input[name="csrfmiddlewaretoken"]');
    const inputFormupTime = $('input#id_formup_time');
    const inputFormupTimestamp = $('input#id_formup_timestamp');
    const inputFleetDoctrine = $('input#id_fleet_doctrine');
    const inputFleetDoctrineUrl = $('input#id_fleet_doctrine_url');

    // const inputFcName = $('input#fcName');
    // const inputFleetName = $('input#fleetName');
    // const inputFormupLocation = $('input#formupLocation');
    // const inputFleetComms = $('input#fleetComms');

    // Text area
    // const textAdditionalInformation = $('textarea#additionalInformation');

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
                $("#id_ping_target").html(data);
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
                $("#id_ping_channel").html(data);
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
                $("#id_fleet_type").html(data);
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
                $("#id_formup_location").after(data);
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
                $("#id_fleet_comms").after(data);
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
                $("#id_fleet_doctrine").after(data);
            }
        });
    };

    /**
     * Convert line breaks into <br>
     *
     * @param {string} string
     * @param {boolean} isXhtml
     */
    const nl2br = (string, isXhtml) => {
        const breakTag = isXhtml || typeof isXhtml === 'undefined' ? '<br />' : '<br>';

        return (string + '').replace(
            /([^>\r\n]?)(\r\n|\n\r|\r|\n)/g,
            '$1' + breakTag + '$2'
        );
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
     * Send an embedded message to a Discord webhook
     *
     * @param {string} webhookUrl Discord webhook URL
     * @param {string} content Message to send to Discord
     * @param {object} embeds Embedded content » https://discohook.org/ - https://leovoel.github.io/embed-visualizer/
     */
    // const sendEmbeddedDiscordPing = (webhookUrl, content, embeds) => {
    //     const request = new XMLHttpRequest();
    //
    //     request.open('POST', webhookUrl);
    //     request.setRequestHeader('Content-type', 'application/json');
    //
    //     const params = {
    //         username: '',
    //         avatar_url: '',
    //         content: content,
    //         embeds: [embeds]
    //     };
    //
    //     request.send(JSON.stringify(params));
    // };

    /**
     * Send a message to a Discord webhook
     *
     * @param {string} webhookUrl Discord webhook URL
     * @param {string} pingText Message to send to Discord
     */
    // const sendDiscordPing = (webhookUrl, pingText) => {
    //     const request = new XMLHttpRequest();
    //
    //     request.open('POST', webhookUrl);
    //     request.setRequestHeader('Content-type', 'application/json');
    //
    //     const params = {
    //         username: '',
    //         avatar_url: '',
    //         content: pingText
    //     };
    //
    //     request.send(JSON.stringify(params));
    // };

    /**
     * Send a message to a Slack webhook
     *
     * @param {string} webhookUrl Slack webhook URL
     * @param {object} payload Message to send to Slack
     */
    // const sendSlackPing = (webhookUrl, payload) => {
    //     $.ajax({
    //         data: 'payload=' + JSON.stringify(payload),
    //         dataType: 'json',
    //         processData: false,
    //         type: 'POST',
    //         url: webhookUrl
    //     });
    // };

    /**
     * Convert hex color code in something Discord can handle
     *
     * @param {string} hexValue
     */
    // const hexToDecimal = (hexValue) => {
    //     return parseInt(hexValue.replace('#', ''), 16);
    // };

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
     * Convert the datepicker info into a URL that the aa-timezones module understands
     *
     * @param {string} formupTime
     */
    // const getTimezonesUrl = (formupTime) => {
    //     const formupTimestamp = getFormupTimestamp(formupTime);
    //
    //     return fleetpingsSettings.url.siteUrl + fleetpingsSettings.url.timezonesUrl + formupTimestamp + '/';
    // };

    /**
     * Create the ping text
     *
     * @param {string} fleetSrpCode SRP code for the fleet, if available
     */
//     const generateFleetPing = (fleetSrpCode) => {
//         const pingTargetSelected = $('option:selected', selectPingTarget);
//         const pingTarget = sanitizeInput(pingTargetSelected.val());
//         const pingTargetText = sanitizeInput(pingTargetSelected.text());
//         const pingChannelSelected = $('option:selected', selectPingChannel);
//         const webhookType = sanitizeInput(pingChannelSelected.data('webhook-type'));
//         const webhookEmbedPing = sanitizeInput(pingChannelSelected.data('webhook-embed'));
//         const fleetTypeSelected = $('option:selected', selectFleetType);
//         const fleetType = sanitizeInput(fleetTypeSelected.val());
//         const webhookEmbedColor = sanitizeInput(fleetTypeSelected.data('embed-color'));
//         const fcName = sanitizeInput(inputFcName.val());
//         const fleetName = sanitizeInput(inputFleetName.val());
//         const formupLocation = sanitizeInput(inputFormupLocation.val());
//         const formupTime = sanitizeInput(inputFormupTime.val());
//         const fleetComms = sanitizeInput(inputFleetComms.val());
//         const fleetDoctrine = sanitizeInput(inputFleetDoctrine.val());
//         const fleetSrp = sanitizeInput($('option:selected', selectFleetSrp).val());
//         const additionalInformation = sanitizeInput(textAdditionalInformation.val());
//
//         // Let's see if we can find a doctrine link
//         let fleetDoctrineLink = null;
//         if (fleetDoctrine !== '') {
//             const selectedLink = $('#fleetDoctrineList [value="' + escapeInput(fleetDoctrine, false) + '"]').data('doctrine-url');
//
//             if ('undefined' !== selectedLink && selectedLink !== '') {
//                 // Houston, we have a link!
//                 fleetDoctrineLink = selectedLink;
//             }
//         }
//
//         // Ping webhooks, if configured
//         let webhookUrl = '';
//
//         if (selectPingChannel.length) {
//             webhookUrl = sanitizeInput(pingChannelSelected.val());
//         }
//
//         $('.aa-fleetpings-no-ping').hide('fast');
//         $('.aa-fleetpings-ping').show('fast');
//
//         let webhookPingTextHeader = '';
//         let webhookPingTextContent = '';
//         let webhookPingTextFooter = '';
//         let pingText = '';
//
//         // Determine pingTarget and pingTargetText
//         let discordPingTarget = '';
//         let webhookPingTarget = '';
//
//         if (pingTarget !== '') {
//             // pingTarget
//             if (pingTarget.indexOf('@') > -1) {
//                 webhookPingTarget = pingTarget;
//                 discordPingTarget = pingTarget;
//             } else {
//                 webhookPingTarget = '<@&' + pingTarget + '>';
//
//                 // pingTargetText
//                 if (pingTargetText.indexOf('@') > -1) {
//                     discordPingTarget = pingTargetText;
//                 } else {
//                     discordPingTarget = '@' + pingTargetText;
//                 }
//             }
//
//             // Separator
//             pingText += ' :: ';
//         }
//
//         // Fleet announcement
//         pingText += '**';
//
//         // Check if it's a pre-ping or not
//         if (checkboxPrePing.is(':checked')) {
//             pingText += '### PRE PING ###';
//             webhookPingTextHeader += '### PRE PING ###';
//
//             if (fleetType !== '') {
//                 pingText += ' / (Upcoming)  ' + fleetType + ' Fleet';
//                 webhookPingTextHeader += ' / (Upcoming) ' + fleetType + ' Fleet';
//             }
//         } else {
//             if (fleetType !== '') {
//                 pingText += fleetType + ' ';
//                 webhookPingTextHeader += fleetType + ' ';
//             }
//
//             pingText += 'Fleet is up';
//             webhookPingTextHeader += 'Fleet is up';
//         }
//
//         // Add fcName if we have one
//         if (fcName !== '') {
//             pingText += ' under ' + fcName;
//             webhookPingTextHeader += ' under ' + fcName;
//         }
//
//         pingText += '**' + '\n';
//
//         // Check if FC name is available
//         if (fcName !== '') {
//             pingText += '\n' + '**FC:** ' + fcName;
//             webhookPingTextContent += '\n' + '**FC:** ' + fcName;
//         }
//
//         // Check if fleet name is available
//         if (fleetName !== '') {
//             pingText += '\n' + '**Fleet Name:** ' + fleetName;
//             webhookPingTextContent += '\n' + '**Fleet Name:** ' + fleetName;
//         }
//
//         // Check if form-up location is available
//         if (formupLocation !== '') {
//             pingText += '\n' + '**Formup Location:** ' + formupLocation;
//             webhookPingTextContent += '\n' + '**Formup Location:** ' + formupLocation;
//         }
//
//         // Check if form-up time is available
//         if (checkboxFormupTimeNow.is(':checked')) {
//             pingText += '\n' + '**Formup Time:** NOW';
//             webhookPingTextContent += '\n' + '**Formup Time:** NOW';
//         } else {
//             if (formupTime !== '') {
//                 pingText += '\n' + '**Formup (EVE Time):** ' + formupTime;
//                 webhookPingTextContent += '\n' + '**Formup (EVE Time):** ' + formupTime;
//
//                 // Get the timestamp and build the link to the timezones module if it's installed
//                 if (fleetpingsSettings.timezonesInstalled === true) {
//                     const timezonesUrl = getTimezonesUrl(formupTime);
//
//                     pingText += ' - ' + timezonesUrl;
//
//                     if (webhookType === 'Discord') {
//                         webhookPingTextContent += ' ([Time Zone Conversion](' + timezonesUrl + '))';
//                     }
//
//                     if (webhookType === 'Slack') {
//                         webhookPingTextContent += ' (<' + timezonesUrl + '|Time Zone Conversion>)';
//                     }
//                 }
//
//                 const formupTimestamp = getFormupTimestamp(formupTime);
//
//                 pingText += '\n' + '**Formup (Local Time):** &lt;t:' + formupTimestamp + ':F&gt;';
//                 webhookPingTextContent += '\n' + '**Formup (Local Time):** <t:' + formupTimestamp + ':F>';
//             }
//         }
//
//         // Check if fleet comms is available
//         if (fleetComms !== '') {
//             pingText += '\n' + '**Comms:** ' + fleetComms;
//             webhookPingTextContent += '\n' + '**Comms:** ' + fleetComms;
//         }
//
//         // Check if doctrine is available
//         if (fleetDoctrine !== '') {
//             pingText += '\n' + '**Ships / Doctrine:** ' + fleetDoctrine;
//             webhookPingTextContent += '\n' + '**Ships / Doctrine:** ' + fleetDoctrine;
//
//             // Grab the doctrine link if there is one
//             if (fleetDoctrineLink !== null) {
//                 pingText += ' - ' + fleetDoctrineLink;
//
//                 if (webhookType === 'Discord') {
//                     webhookPingTextContent += ' ([Doctrine Link](' + fleetDoctrineLink + '))';
//                 }
//
//                 if (webhookType === 'Slack') {
//                     webhookPingTextContent += ' (<' + fleetDoctrineLink + '|Doctrine Link>)';
//                 }
//             }
//         }
//
//         // Check if srp is available
//         if (fleetSrp !== '') {
//             pingText += '\n' + '**SRP:** ' + fleetSrp;
//             webhookPingTextContent += '\n' + '**SRP:** ' + fleetSrp;
//
//             if (fleetSrp === 'Yes' && fleetSrpCode !== '') {
//                 pingText += ' (SRP Code: ' + fleetSrpCode + ')';
//                 webhookPingTextContent += ' (SRP Code: ' + fleetSrpCode + ')';
//             }
//         }
//
//         // Check if additional information is available
//         if (additionalInformation !== '') {
//             pingText += '\n\n' + '**Additional Information**:' + '\n' + additionalInformation;
//             webhookPingTextContent += '\n\n' + '**Additional Information**:' + '\n' + additionalInformation;
//         }
//
//         if (webhookType === 'Discord') {
//             $('.aa-fleetpings-ping-text').html(
//                 '<p>' + nl2br(discordPingTarget + pingText, false) + '</p>'
//             );
//         }
//
//         if (webhookType === 'Slack') {
//             $('.aa-fleetpings-ping-text').html(
//                 '<p>' + nl2br(discordPingTarget + pingText.split('**').join('*'), false) + '</p>'
//             );
//         }
//
//         // Ping it directly if a webhook is selected
//         if (webhookUrl !== '') {
//             // add ping creator at the end
//             if (fleetpingsSettings.pingCreator !== '') {
//                 pingText += '\n\n' + '*(Ping sent by: ' + fleetpingsSettings.pingCreator + ')*';
//                 webhookPingTextFooter = '(Ping sent by: ' + fleetpingsSettings.pingCreator + ')';
//             }
//
//             // Default embed color
//             let embedColor = '#faa61a';
//
//             if (fleetType !== '' && embedColor !== '') {
//                 embedColor = webhookEmbedColor;
//             }
//
//             // Send the ping to Discord
//             if (webhookType === 'Discord') {
//                 if ('undefined' !== webhookEmbedPing && webhookEmbedPing === 'True') {
//                     if (pingTarget !== '') {
//                         webhookPingTarget += ' :: ';
//                     }
//
//                     sendEmbeddedDiscordPing(
//                         webhookUrl,
//                         webhookPingTarget + '**' + webhookPingTextHeader + '**' + '\n' + '** **',
//                         {
//                             'title': '**.: Fleet Details :.**',
//                             'description': webhookPingTextContent,
//                             'color': hexToDecimal(embedColor),
//                             'footer': {
//                                 'text': webhookPingTextFooter
//                             }
//                         }
//                     );
//                 } else {
//                     sendDiscordPing(webhookUrl, webhookPingTarget + pingText);
//                 }
//             }
//
//             // Send the ping to Discord
//             if (webhookType === 'Slack') {
//                 let slackEmbedPingTarget = '';
//
//                 if (pingTarget !== '') {
//                     slackEmbedPingTarget = '<' + webhookPingTarget.replace('@everyone', '!channel').replace('@', '!') + '> :: ';
//                 }
//
//                 /**
//                  * Payload to send to Slack
//                  *
//                  * @type {{attachments: [{color: string, footer: string, pretext: string, text: string, fallback: string}]}}
//                  */
//                 const payload = {
//                     'attachments': [
//                         {
//                             'fallback': pingText,
//                             'color': embedColor,
//                             'pretext': slackEmbedPingTarget + '*' + webhookPingTextHeader + '*',
//                             'text': '*.: Fleet Details :.*' + '\n' + webhookPingTextContent.split('**').join('*'),
//                             'footer': webhookPingTextFooter
// //                            'footer_icon': 'https://platform.slack-edge.com/img/default_application_icon.png'
//                         }
//                     ]
//                 };
//
//                 sendSlackPing(webhookUrl, payload);
//             }
//
//             // Tell the FC that it's already pinged
//             showSuccess(
//                 fleetpingsTranslations.ping.success,
//                 '.aa-fleetpings-ping-copyresult'
//             );
//         }
//     };

    /**
     * Craete a fleet ping with SRP
     *
     * @param {string} fleetName
     * @param {string} fleetDoctrine
     * @returns {boolean}
     */
    // const generateFleetPingWithSrp = (fleetName, fleetDoctrine) => {
    //     // Check for mandatory fields
    //     if (fleetpingsSettings.srpModuleAvailableToUser === true) {
    //         if (fleetName !== '' && fleetDoctrine !== '') {
    //             // Create SRP link
    //             const srpAjaxUrl = fleetpingsSettings.url.srpAjaxUrl;
    //             let srpCode = '';
    //
    //             $.ajax({
    //                 url: srpAjaxUrl,
    //                 type: 'post',
    //                 data: {
    //                     fleet_doctrine: fleetDoctrine,
    //                     fleet_name: fleetName
    //                 },
    //                 headers: {
    //                     'X-CSRFToken': sanitizeInput(
    //                         inputCsrfMiddlewareToken.val()
    //                     )
    //                 }
    //             }).done((result) => {
    //                 srpCode = result.srp_code;
    //
    //                 // Create fleet ping
    //                 generateFleetPing(srpCode);
    //
    //                 // Let the user know that an optimer has been created
    //                 // and close potentially former error messages
    //                 closeMessageElement('.alert-message-error', 0);
    //                 showSuccess(
    //                     fleetpingsTranslations.srp.created,
    //                     '.fleetpings-create-srp-link-message'
    //                 );
    //             });
    //
    //             // Re-set checkbox
    //             checkboxCreateSrpLink.prop('checked', false);
    //         } else {
    //             showError(
    //                 fleetpingsTranslations.srp.error.missingFields,
    //                 '.fleetpings-create-srp-link-message'
    //             );
    //         }
    //
    //         return true;
    //     } else {
    //         return false;
    //     }
    // };

    /**
     *
     * @param {string} fleetName
     * @param {string} fleetDoctrine
     * @param {string} formupLocation
     * @param {string} formupTime
     * @param {string} fcName
     * @returns {boolean}
     */
    // const generateFleetPingWithOptimer = (fleetName, fleetDoctrine, formupLocation, formupTime, fcName) => {
    //     if (fleetpingsSettings.optimerInstalled === true) {
    //         if (fleetName !== '' && fleetDoctrine !== '' && formupLocation !== '' && formupTime !== '' && fcName !== '') {
    //             const optimerAjaxUrl = fleetpingsSettings.url.optimerAjaxUrl;
    //
    //             $.ajax({
    //                 url: optimerAjaxUrl,
    //                 type: 'post',
    //                 data: {
    //                     fleet_doctrine: fleetDoctrine,
    //                     formup_location: formupLocation,
    //                     formup_time: formupTime,
    //                     fleet_name: fleetName,
    //                     fleet_commander: fcName
    //                 },
    //                 headers: {
    //                     'X-CSRFToken': inputCsrfMiddlewareToken.val()
    //                 }
    //             });
    //
    //             // Re-set checkbox
    //             checkboxCreateOptimer.prop('checked', false);
    //
    //             // Create fleet ping
    //             generateFleetPing('');
    //
    //             // Let the user know that an optimer has been created
    //             // and close potentially former error messages
    //             closeMessageElement('.alert-message-error', 0);
    //             showSuccess(
    //                 fleetpingsTranslations.optimer.created,
    //                 '.fleetpings-create-optimer-message'
    //             );
    //         } else {
    //             showError(
    //                 fleetpingsTranslations.optimer.error.missingFields,
    //                 '.fleetpings-create-optimer-message'
    //             );
    //         }
    //
    //         return true;
    //     } else {
    //         return false;
    //     }
    // };

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
    $("form").submit((event) => {
    // $('button#createPingText').on('click', () => {
        // const fleetName = sanitizeInput(inputFleetName.val());
        // const fleetDoctrine = sanitizeInput(inputFleetDoctrine.val());
        // const formupTime = sanitizeInput(inputFormupTime.val());
        // const fcName = sanitizeInput(inputFcName.val());
        // const formupLocation = sanitizeInput(inputFormupLocation.val());

        // let pingCreated = false;

        // Check if we should create an SRP link
        // if (checkboxCreateSrpLink.is(':checked') && checkboxFormupTimeNow.is(':checked')) {
        //     pingCreated = generateFleetPingWithSrp(fleetName, fleetDoctrine);
        // }

        // Check if we should create an optimer
        // if (checkboxPrePing.is(':checked') && checkboxCreateOptimer.is(':checked')) {
        //     pingCreated = generateFleetPingWithOptimer(
        //         fleetName, fleetDoctrine, formupLocation, formupTime, fcName
        //     );
        // }

        // if (pingCreated === false) {
        //     generateFleetPing('');
        // }


        // Stop the browser from sending the form, we take care of it
        event.preventDefault();

        // const pingTargetSelected = $('option:selected', selectPingTarget);
        // const pingTarget = sanitizeInput(pingTargetSelected.val());
        // const pingTargetText = sanitizeInput(pingTargetSelected.text());
        // const pingChannelSelected = $('option:selected', selectPingChannel);
        // const webhookType = sanitizeInput(pingChannelSelected.data('webhook-type'));
        // const webhookEmbedPing = sanitizeInput(pingChannelSelected.data('webhook-embed'));
        // const fcName = sanitizeInput(inputFcName.val());
        // const fleetName = sanitizeInput(inputFleetName.val());
        // const formupLocation = sanitizeInput(inputFormupLocation.val());
        // const formupTime = sanitizeInput(inputFormupTime.val());
        // const fleetComms = sanitizeInput(inputFleetComms.val());

        // Get the form data
        let formData = $('#aa-fleetping-form').serializeArray().reduce((obj, item) => {
            obj[item.name] = item.value;

            return obj;
        }, {});

        // Add some additional info
        // fleetDoctrineUrl
        // const fleetDoctrine = sanitizeInput(inputFleetDoctrine.val());
        // const fleetDoctrineUrl = $(
        //     '#fleetDoctrineList [value="' + escapeInput(fleetDoctrine, false) + '"]'
        // ).data('doctrine-url');
        // formData.fleetDoctrineUrl = fleetDoctrineUrl || '';

        console.table(formData);

        $.ajax({
            url: fleetpingsSettings.url.fleetPing,
            type: 'post',
            data: formData,
            headers: {
                'X-CSRFToken': inputCsrfMiddlewareToken.val()
            },
            success: (data) => {
                console.log(data);

                $('.aa-fleetpings-no-ping').hide('fast');
                $('.aa-fleetpings-ping').show('fast');

                $('.aa-fleetpings-ping-text').html(
                    '<p>' + nl2br(data.context.ping_target + data.context.ping_text, false) + '</p>'
                );
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
