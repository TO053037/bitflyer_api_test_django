async function getCandlesticks() {
    console.log('get func');
    const day_period = 10;
    const query_params = new URLSearchParams({
        'day_period': day_period,
    })
    const resJson = await fetch(getCandlesticksUrl + '?' + query_params);
    const res = await resJson.json();
    return res;
}