const SUCCESS_MESSAGE = 'Model initialized.';

const root = document.getElementById('root');

const showInRoot = elements => {
    root.replaceChildren(...elements);
};

const imagFileToBase64 = imageFile => {
    const reader = new FileReader();
    reader.readAsDataURL(imageFile);

    return new Promise(resolve => {
        reader.onload = () => resolve(reader.result);
    });
};

const showLoader = () => {
    const loaderTextPrefix = document.createTextNode('The model is ');
    const loaderTextSuffix = document.createTextNode('Please Wait. Thank you.');

    const loaderElement = document.createElement('div');
    loaderElement.className = 'loader-initial';

    const loaderContainer = document.createElement('div');
    loaderContainer.className = 'loader-container';

    loaderContainer.appendChild(loaderTextPrefix);
    loaderContainer.appendChild(loaderElement);
    loaderContainer.appendChild(loaderTextSuffix);

    showInRoot([loaderContainer]);
};

const getUploadButton = retry => {
    const fileInputElement = document.createElement('input');
    fileInputElement.className = 'file-upload-input';
    fileInputElement.type = 'file';
    fileInputElement.accept = 'image/*';

    fileInputElement.addEventListener('change', e => showImageUploadedState(e));

    const buttonElement = document.createElement('button');
    buttonElement.className = 'upload-button';
    buttonElement.textContent = retry ? 'Upload another image' : 'Upload an image';

    buttonElement.appendChild(fileInputElement);

    buttonElement.addEventListener('click', () => fileInputElement.click());

    return buttonElement;
};

const getUploadedImage = imageUrl => {
    const imageContainer = document.createElement('div');
    imageContainer.className = 'image-container';

    const imageElement = document.createElement("img");
    imageElement.className = 'uploaded-image';
    imageElement.src = imageUrl;

    imageContainer.replaceChildren(imageElement);

    return imageContainer;
};

const getCssLoader = () => {
    const loaderElement = document.createElement('div');
    loaderElement.className = 'loader';

    return loaderElement;
}

const getPrediction = async imageUrl => {
    const actionButtonContainer = document.querySelector('.action-button-container');
    actionButtonContainer.removeChild(actionButtonContainer.lastChild);
    actionButtonContainer.appendChild(getCssLoader());

    const predictedResult = await callAPI(API_INFO.PREDICT, { "image": imageUrl });

    const predictedLetter = predictedResult.letter;

    const predictedLetterElement = document.createElement('div');
    predictedLetterElement.className = 'predicted-letter';
    predictedLetterElement.textContent = predictedLetter;

    const predictedResultElement = document.createElement('div');
    predictedResultElement.className = 'predicted-result';
    predictedResultElement.textContent = 'Prediction Result';

    predictedResultElement.appendChild(predictedLetterElement);

    actionButtonContainer.removeChild(actionButtonContainer.lastChild);
    actionButtonContainer.appendChild(predictedResultElement);
}

const getImageActionButtons = imageUrl => {
    const actionButtonContainer = document.createElement('div');
    actionButtonContainer.className = 'action-button-container';

    const uploadButton = getUploadButton(true);

    const predictButton = document.createElement('button');
    predictButton.className = 'predict-button';
    predictButton.textContent = 'Predict';
    predictButton.onclick = () => getPrediction(imageUrl);

    actionButtonContainer.replaceChildren(uploadButton, predictButton);

    return actionButtonContainer;
}

const showImageUploadedState = async event => {
    const [imageFile] = event.target.files;

    const imageUrl = await imagFileToBase64(imageFile);
    const uploadedImage = getUploadedImage(imageUrl);
    const actionButtons = getImageActionButtons(imageUrl);

    showInRoot([uploadedImage, actionButtons]);
};

const showError = errorMessage => {
    const errorElement = document.createElement('div');
    errorElement.className = 'error';
    errorElement.textContent = errorMessage;
    
    showInRoot([errorElement]);
};

const initialize = async () => {
    showLoader();

    const initializationResponse = await callAPI(API_INFO.INITIALIZE, null);
    const responseMessage = initializationResponse.message;

    if(responseMessage == SUCCESS_MESSAGE) {
        const uploadButton = getUploadButton(false);
        showInRoot([uploadButton]);
    } else {
        showError(responseMessage);
    }
};

window.addEventListener("load", initialize);