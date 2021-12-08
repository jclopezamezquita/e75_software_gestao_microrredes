import { Injectable, Inject, InjectionToken } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { Milp_parameters } from "./milp_parameter.model";
import { catchError } from "rxjs/operators";
import { Economic_dispatch } from "./economic_dispatch.model";

export const REST_URL = new InjectionToken("rest_url");

@Injectable()
export class RestDataSource {
    constructor(private http: HttpClient,
        @Inject(REST_URL) private url: string) { }

    getData_Economic_dispatch(): Observable<Economic_dispatch[]> {
        return this.sendRequest<Economic_dispatch[]>("GET", 
            `${this.url}/v1/api/economic_dispatch`);
    }

    getData_Milp_parameters(): Observable<Milp_parameters[]> {
        return this.sendRequest<Milp_parameters[]>("GET", 
            `${this.url}/v1/api/milp_parameters`);
    }

    updateData_Milp_parameters(milp_parameters: Milp_parameters): Observable<Milp_parameters> {
        return this.sendRequest<Milp_parameters>("PUT",
            `${this.url}/v1/api/milp_parameters/1`, milp_parameters);
    }

    private sendRequest<T>(verb: string, url: string, body?: any)
        : Observable<T> {

        let myHeaders = new HttpHeaders();
        myHeaders = myHeaders.set("accept", "application/json");

        return this.http.request<T>(verb, url, {
            body: body,
            headers: myHeaders
        }).pipe(catchError((error: Response) => 
             throwError(`Network Error: ${error.statusText} (${error.status})`)));
    }

}
