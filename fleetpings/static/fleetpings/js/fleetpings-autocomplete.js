/* global fleetpingsSettings */

import Autocomplete from '/static/fleetpings/libs/bootstrap5-autocomplete/1.1.25/autocomplete.min.js';

// Selects
const selectPingTarget = $('select#id_ping_target');
const selectPingChannel = $('select#id_ping_channel');
const selectFleetType = $('select#id_fleet_type');

// Input fields
const inputFleetComms = $('input#id_fleet_comms');
const inputFormupLocation = $('input#id_formup_location');
const inputFleetDoctrine = $('input#id_fleet_doctrine');

/**
 * Get data from a given ajax URL
 *
 * @param {string} url The URL to query
 * @returns {Promise<string>}
 */
const getDataFromAjaxUrl = async (url) => {
    'use strict';

    const response = await fetch(url);

    if (!response.ok) {
        const message = `An error has occurred: ${response.status}`;

        throw new Error(message);
    }

    return await response.text();
};

const opts = {
    onSelectItem: console.log,
};

/**
 * Get user dropdown data from the server
 */
const getUserDropdownData = () => {
    'use strict';

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
    });

    getDataFromAjaxUrl(fleetpingsSettings.url.fleetDoctrines).then(fleetDoctrines => {
        $(inputFleetDoctrine).after(fleetDoctrines);
    });
};


getUserDropdownData();
