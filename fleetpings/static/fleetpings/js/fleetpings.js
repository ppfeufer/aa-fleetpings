/* global fleetpingsSettings, ClipboardJS, fetchGet, fetchPost */

import Autocomplete from '/static/fleetpings/libs/bootstrap5-autocomplete/1.1.39/autocomplete.min.js';

$(document).ready(() => {
    'use strict';

    /* DOM Elements Cache */
    const elements = {
        // Checkboxes
        prePing: $('#id_pre_ping'),
        formupTimeNow: $('#id_formup_now'),
        createSrpLink: $('#id_srp_link'),
        createOptimer: $('#id_optimer'),
        fleetSrp: $('#id_srp'),

        // Selects
        pingTarget: $('#id_ping_target'),
        pingChannel: $('#id_ping_channel'),
        fleetType: $('#id_fleet_type'),

        // Inputs
        csrfToken: $('input[name="csrfmiddlewaretoken"]'),
        fleetComms: $('#id_fleet_comms'),
        fleetCommander: $('#id_fleet_commander'),
        fleetName: $('#id_fleet_name'),
        formupTime: $('#id_formup_time'),
        formupTimestamp: $('#id_formup_timestamp'),
        formupLocation: $('#id_formup_location'),
        fleetDoctrine: $('#id_fleet_doctrine'),
        fleetDoctrineUrl: $('#id_fleet_doctrine_url'),
        webhookEmbedColor: $('#id_webhook_embed_color')
    };

    /* Initialize datetime picker */
    elements.formupTime.datetimepicker({
        lang: fleetpingsSettings.dateTimeLocale,
        maskInput: true,
        format: 'Y-m-d H:i',
        dayOfWeekStart: 1,
        step: 15
    });

    /* Utility Functions */
    const utils = {
        /**
         * Sanitize input by removing HTML tags.
         *
         * @param {string} input The input string to sanitize.
         * @returns {string} The sanitized string with HTML tags removed.
         */
        sanitizeInput: (input) => {
            return input && input.replace ? input.replace(/<[^>]*>/g, '') : input;
        },

        /**
         * Escape input by replacing special characters with HTML entities or escaped characters.
         *
         * @param {string} input The input string to escape.
         * @param {boolean} [quotesToEntities=false] If true, replaces double quotes with HTML entities; otherwise, escapes them.
         * @returns {string} The escaped string with special characters replaced.
         */
        escapeInput: (input, quotesToEntities = false) => {
            if (!input) {
                return input;
            }

            const escaped = utils.sanitizeInput(input).replace(/&/g, '&amp;');

            return quotesToEntities ? escaped.replace(/"/g, '&quot;') : escaped.replace(/"/g, '\\"');
        },

        /**
         * Get the timestamp for the formup time.
         * This function converts the formup time to a Unix timestamp in seconds.
         *
         * @param {string} formupTime The formup time in a format recognized by the Date constructor.
         * @returns {number} The Unix timestamp in seconds.
         */
        getFormupTimestamp: (formupTime) => {
            const formupDateTime = new Date(formupTime);

            return (formupDateTime.getTime() - formupDateTime.getTimezoneOffset() * 60 * 1000) / 1000;
        },

        /**
         * Display a message in the specified element.
         * This function creates an alert message with a close button and optional auto-close functionality.
         *
         * @param {string} message The message to display.
         * @param {string} element The selector for the element where the message will be displayed.
         * @param {string} [type=success] The type of message ('success' or 'error').
         * @param {boolean} [autoClose=true] Whether to automatically close the message after a certain time.
         * @return {void}
         */
        showMessage: (message, element, type = 'success', autoClose = true) => {
            const alertType = type === 'success' ? 'alert-success' : 'alert-danger';
            const closeAfter = type === 'success' ? 10000 : 9999000;
            const containerClasses = `alert ${alertType} alert-dismissible alert-message-${type} align-items-center fade show`;

            $(element).html(`<div class="${containerClasses}">${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`);

            if (autoClose) {
                $(`${element} > .alert-message-${type}`).fadeTo(closeAfter, 500).slideUp(500, () => {
                    $(`${element} > .alert-message-${type}`).remove();
                });
            }
        }
    };

    /* Data Loading Functions */
    const dataLoader = {
        /**
         * Load data into a select element from a given URL.
         *
         * @param {string} url The URL to fetch data from.
         * @param {string} target The selector for the target select element where the data will be loaded.
         * @returns {Promise<void>} A promise that resolves when the data is loaded.
         */
        loadSelectData: async (url, target) => {
            try {
                const data = await fetchGet({url, responseIsJson: false});

                $(target).html(data);
            } catch (error) {
                console.error(`Error loading data from ${url}:`, error);
            }
        },

        /**
         * Load autocomplete data from a given URL and create an autocomplete instance.
         *
         * @param {string} url The URL to fetch autocomplete data from.
         * @param {HTMLElement} inputElement The input element where the autocomplete will be attached.
         * @param {string} elementId The ID of the element where the autocomplete will be created.
         * @returns {Promise<void>} A promise that resolves when the autocomplete data is loaded and the instance is created.
         */
        loadAutocompleteData: async (url, inputElement, elementId) => {
            try {
                const data = await fetchGet({url, responseIsJson: false});

                if (data.trim()) {
                    dataLoader.createAutocomplete(inputElement, elementId, data);
                }
            } catch (error) {
                console.error(`Error loading autocomplete data from ${url}:`, error);
            }
        },

        /**
         * Create an autocomplete instance after the specified element.
         *
         * @param {HTMLElement} afterElement The element after which the autocomplete will be created.
         * @param {string} elementId The ID of the input element for the autocomplete.
         * @param {string} data The HTML data to be used for the autocomplete options.
         * @returns {void}
         */
        createAutocomplete: (afterElement, elementId, data) => {
            const options = {
                onSelectItem: (selected_item, datalist) => {
                    if (datalist.e.datalist === 'fleet-doctrine-list') {
                        handlers.setFleetDoctrineUrl();
                    }
                },
                preventBrowserAutocomplete: true,
                onRenderItem: (item, label) => {
                    return `<l-i set="fl" name="${item.value.toLowerCase()}" size="16"></l-i> ${label}`;
                }
            };

            afterElement.after(data);

            const autoComplete = new Autocomplete( // eslint-disable-line no-unused-vars
                document.getElementById(elementId),
                options
            );
        },

        /**
         * Initialize the data loader by loading all necessary data for the form.
         *
         * @returns {Promise<void>} A promise that resolves when all data is loaded.
         */
        initialize: async () => {
            // Load select dropdowns
            await Promise.all([
                dataLoader.loadSelectData(fleetpingsSettings.url.pingTargets, elements.pingTarget),
                dataLoader.loadSelectData(fleetpingsSettings.url.pingWebhooks, elements.pingChannel),
                dataLoader.loadSelectData(fleetpingsSettings.url.fleetTypes, elements.fleetType)
            ]);

            // Load autocomplete data
            await Promise.all([
                dataLoader.loadAutocompleteData(fleetpingsSettings.url.formupLocations, elements.formupLocation, 'id_formup_location'),
                dataLoader.loadAutocompleteData(fleetpingsSettings.url.fleetComms, elements.fleetComms, 'id_fleet_comms'),
                dataLoader.loadAutocompleteData(fleetpingsSettings.url.fleetDoctrines, elements.fleetDoctrine, 'id_fleet_doctrine')
            ]);
        }
    };

    /* Event Handlers */
    const handlers = {
        /**
         * Update the visibility of checkboxes based on the current state of other checkboxes.
         *
         * @returns {void}
         */
        updateCheckboxVisibility: () => {
            const isPrePingChecked = elements.prePing.is(':checked');
            const isFormupNow = elements.formupTimeNow.is(':checked');
            const isFleetSrpChecked = elements.fleetSrp.is(':checked');

            // Handle Optimer visibility
            if (fleetpingsSettings.optimerInstalled) {
                if (isPrePingChecked) {
                    $('.fleetpings-create-optimer').show('fast');
                } else {
                    $('.fleetpings-create-optimer').hide('fast');

                    elements.createOptimer.prop('checked', false);
                }
            }

            // Handle SRP Link visibility
            if (fleetpingsSettings.srpModuleAvailableToUser) {
                const shouldShowSrpLink = isFormupNow && isFleetSrpChecked;
                console.log(`SRP Link visibility: ${shouldShowSrpLink}`);

                if (shouldShowSrpLink) {
                    $('.fleetpings-create-srp-link').show('fast');
                } else {
                    $('.fleetpings-create-srp-link').hide('fast');

                    elements.createSrpLink.prop('checked', false);
                }
            }
        },

        /**
         * Set the fleet doctrine URL based on the selected doctrine.
         *
         * @returns {void}
         */
        setFleetDoctrineUrl: () => {
            const fleetDoctrine = utils.sanitizeInput(elements.fleetDoctrine.val());

            if (!fleetDoctrine) {
                elements.fleetDoctrineUrl.val(null);

                return;
            }

            const selectedLink = $(`#fleet-doctrine-list [value="${utils.escapeInput(fleetDoctrine)}"]`).data('doctrine-url');

            elements.fleetDoctrineUrl.val(selectedLink || null);
        },

        /**
         * Submit the fleet ping form.
         * This function handles the form submission, validates the input fields, and sends the data to the server.
         * It also handles the response and displays appropriate messages to the user.
         *
         * @param {Event} event The event object from the form submission.
         * @returns {Promise<void>} A promise that resolves when the form submission is complete.
         */
        submitForm: async (event) => {
            event.preventDefault();

            $('.fleetpings-form-message div').remove();

            // Validation
            const validateFields = (fields, errorMessage) => {
                if (fields.some(field => !field)) {
                    utils.showMessage(errorMessage, '.fleetpings-form-message', 'error');

                    return false;
                }

                return true;
            };

            if (fleetpingsSettings.srpModuleAvailableToUser && elements.createSrpLink.is(':checked')) {
                if (!validateFields(
                    [elements.fleetName.val(), elements.fleetDoctrine.val()],
                    fleetpingsSettings.translation.srp.error.missingFields
                )) {
                    return;
                }
            }

            if (fleetpingsSettings.optimerInstalled && elements.createOptimer.is(':checked')) {
                if (!validateFields(
                    [
                        elements.fleetName.val(), elements.fleetDoctrine.val(),
                        elements.formupLocation.val(), elements.formupTime.val(),
                        elements.fleetCommander.val()
                    ],
                    fleetpingsSettings.translation.optimer.error.missingFields
                )) {
                    return;
                }
            }

            try {
                const formData = $('#aa-fleetping-form').serializeArray().reduce((obj, item) => {
                    obj[item.name] = item.value;

                    return obj;
                }, {});

                const data = await fetchPost({
                    url: fleetpingsSettings.url.fleetPing,
                    csrfToken: elements.csrfToken.val(),
                    payload: formData,
                    responseIsJson: true
                });

                if (data.success) {
                    $('.aa-fleetpings-no-ping').hide('fast');
                    $('.aa-fleetpings-ping').show('fast');
                    $('.aa-fleetpings-ping-text').html(data.ping_context);

                    if (data.message) {
                        utils.showMessage(
                            data.message,
                            '.fleetpings-form-message'
                        );
                    }
                } else {
                    utils.showMessage(
                        data.message || 'Something went wrong, no details given.',
                        '.fleetpings-form-message',
                        'error'
                    );
                }
            } catch (error) {
                console.error('Error:', error.message);

                utils.showMessage(
                    error.message || 'Something went wrong, no details given.',
                    '.fleetpings-form-message',
                    'error'
                );
            }
        }
    };

    /* Event Listeners */
    elements.pingTarget.on('change', () => {
        $('.hint-ping-everyone').toggle(elements.pingTarget.val() === '@everyone');
    });

    elements.formupTime.on('change', () => {
        const timestamp = utils.getFormupTimestamp(utils.sanitizeInput(elements.formupTime.val()));

        elements.formupTimestamp.val(timestamp);
    });

    elements.fleetType.on('change', () => {
        const selectedOption = $('option:selected', elements.fleetType);
        const embedColor = utils.sanitizeInput(selectedOption.data('embed-color')) || null;

        elements.webhookEmbedColor.val(embedColor);
    });

    elements.prePing.on('change', () => {
        const isChecked = elements.prePing.is(':checked');

        elements.formupTimeNow.prop('checked', !isChecked);
        elements.formupTime.prop('disabled', !isChecked);

        handlers.updateCheckboxVisibility();
    });

    elements.formupTimeNow.on('change', () => {
        const isChecked = elements.formupTimeNow.is(':checked');

        elements.prePing.prop('checked', !isChecked);
        elements.formupTime.prop('disabled', isChecked);

        handlers.updateCheckboxVisibility();
    });

    if (fleetpingsSettings.srpModuleAvailableToUser) {
        elements.fleetSrp.on('change', handlers.updateCheckboxVisibility);
    }

    $('form').on('submit', handlers.submitForm);

    $('#copyFleetPing').on('click', () => {
        const clipboard = new ClipboardJS('#copyFleetPing');

        clipboard
            .on('success', (e) => {
                utils.showMessage(
                    fleetpingsSettings.translation.copyToClipboard.success,
                    '.aa-fleetpings-ping-copyresult'
                );

                e.clearSelection();

                clipboard.destroy();
            })
            .on('error', () => {
                utils.showMessage(
                    fleetpingsSettings.translation.copyToClipboard.error,

                    '.aa-fleetpings-ping-copyresult',
                    'error'
                );

                clipboard.destroy();
            });
    });

    /* Initialize */
    handlers.updateCheckboxVisibility();
    dataLoader.initialize();
});
