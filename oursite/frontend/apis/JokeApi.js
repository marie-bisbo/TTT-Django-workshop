import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class JokeApi {
    submit(searchTerm) {
        const url = '/api/submit/';
        const data = { 'searchTerm': searchTerm };
        return axios.post(url, data)
            .then(response => response.data)
            .catch((e) => {
                console.log(e);
            });
    }
}