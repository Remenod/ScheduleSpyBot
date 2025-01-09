const urlParams = new URLSearchParams(window.location.search);
const currWeekGid = urlParams.get('currWeekGid') || '0';

const iframeSrc = `https://docs.google.com/spreadsheets/d/106PsLWpv_rWHSS8qCghliTpv6kZVTRiabmFyeWN6zH4/htmlview?widget=true&headers=true&gid=${currWeekGid}#gid=${currWeekGid}`;

document.getElementById('scheduleIframe').src = iframeSrc;
