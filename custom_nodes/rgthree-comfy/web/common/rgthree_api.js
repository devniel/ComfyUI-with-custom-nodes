class RgthreeApi {
    constructor(baseUrl) {
        this.getCheckpointsPromise = null;
        this.getSamplersPromise = null;
        this.getSchedulersPromise = null;
        this.getLorasPromise = null;
        this.getWorkflowsPromise = null;
        this.baseUrl = baseUrl || './rgthree/api';
    }
    apiURL(route) {
        return `${this.baseUrl}${route}`;
    }
    fetchApi(route, options) {
        return fetch(this.apiURL(route), options);
    }
    async fetchJson(route, options) {
        const r = await this.fetchApi(route, options);
        return await r.json();
    }
    async postJson(route, json) {
        const body = new FormData();
        body.append("json", JSON.stringify(json));
        return await rgthreeApi.fetchJson(route, { method: "POST", body });
    }
    getLoras(force = false) {
        if (!this.getLorasPromise || force) {
            this.getLorasPromise = this.fetchJson("/loras", { cache: "no-store" });
        }
        return this.getLorasPromise;
    }
}
export const rgthreeApi = new RgthreeApi();
