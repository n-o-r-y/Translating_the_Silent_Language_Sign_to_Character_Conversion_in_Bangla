const API_BASE_URL = 'http://localhost:8000/';

const API_INFO = {
    INITIALIZE: {
        endpoint: 'initialize',
        method: 'GET',
    },
    PREDICT: {
        endpoint: 'get_prediction',
        method: 'POST',
    },
};

const callUploadAPI = async (imageURL, callback) => {
    const rawImage = JSON.stringify({ "image": imageURL });
    const requestOptions = {
        method: 'POST',
        body: rawImage,
    };

    const response = await fetch('http://localhost:8000/upload_image', requestOptions);
    const responseData = await response.json();

    callback(responseData);
};

const callAPI = async (apiInfo, body) => {
    const {endpoint, method} = apiInfo;

    const serializedData = JSON.stringify(body);

    const requestOptions = body ? {method, body: serializedData} : {method};

    try {
        const response = await fetch(API_BASE_URL + endpoint, requestOptions);
        const responseData = await response.json();

        return responseData;
    } catch (error) {
        return error;
    }
};
