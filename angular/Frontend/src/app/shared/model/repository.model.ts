import { Injectable } from "@angular/core";
import { Milp_parameters } from "./milp_parameter.model";
import { Economic_dispatch } from "./economic_dispatch.model";
import { EV_parameters } from "./ev_parameters.model";
import { RestDataSource } from "./rest.datasource";

@Injectable()
export class Model {
    public milp_parameters: Milp_parameters[] = new Array<Milp_parameters>();
    public economic_dispatch: Economic_dispatch[] = new Array<Economic_dispatch>();
    public ev_parameters: EV_parameters[] = new Array<EV_parameters>();
    private locator_Milp_parameters = (p: Milp_parameters, id: number) => p.id == id;
    private locator_EV_parameters = (p: EV_parameters, id: number) => p.id == id;
    private locator_Economic_dispatch = (p: Economic_dispatch, id: number) => p.id == id;

    constructor(private dataSource: RestDataSource) {
        this.dataSource.getData_Milp_parameters().subscribe(data => this.milp_parameters = data);
        this.dataSource.getData_Economic_dispatch().subscribe(data => this.economic_dispatch = data);
        this.dataSource.getData_EV_parameters().subscribe(data => this.ev_parameters = data);
    }

    getEconomicDispatches(): Economic_dispatch[] {
        return this.economic_dispatch;
    }

    getEconomicDispatch(id: number): Economic_dispatch {
        return this.economic_dispatch.find(p => this.locator_Economic_dispatch(p, id));
    }

    getMilpParameters(): Milp_parameters[] {
        return this.milp_parameters;
    }

    getMilpParameter(id: number): Milp_parameters {
        return this.milp_parameters.find(p => this.locator_Milp_parameters(p, id));
    }

    updateMilpParameters(milp_parameters: Milp_parameters) {
        this.dataSource.updateData_Milp_parameters(milp_parameters).subscribe(p => {
            let index = this.milp_parameters
                .findIndex(item => this.locator_Milp_parameters(item, p.id));
            this.milp_parameters.splice(index, 1, p);
        });
    }

    getEVParameters(): EV_parameters[] {
        return this.ev_parameters;
    }

    getEVParameter(id: number): EV_parameters {
        return this.ev_parameters.find(p => this.locator_EV_parameters(p, id));
    }

    updateEVParameters(ev_parameters: EV_parameters) {
        this.dataSource.updateData_EV_parameters(ev_parameters).subscribe(p => {
            let index = this.ev_parameters
                .findIndex(item => this.locator_EV_parameters(item, p.id));
            this.ev_parameters.splice(index, 1, p);
        });
    }
}