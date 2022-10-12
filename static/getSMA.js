async function getSMA(dayPeriod) {
    console.log('get func');
    const day_period = 10;
    const query_params = new URLSearchParams({
        'day_period': dayPeriod,
    })
    const resJson = await fetch(getSMAUrl + '?' + query_params);
    const res = await resJson.json();
    return res;
}