import '../../node_modules/fomantic-ui-css/semantic.css'
import '../../node_modules/flatpickr/dist/flatpickr.css'
import './main.css';

const jQuery = require("jquery")
window.$ = window.jQuery = jQuery;

const flatpickr = require("flatpickr");
const German = require("flatpickr/dist/l10n/de.js").default.de;
flatpickr.localize(German);

require("chart.js")
require("fomantic-ui-css/semantic")