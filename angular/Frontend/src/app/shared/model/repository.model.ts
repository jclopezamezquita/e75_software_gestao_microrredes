import { Injectable } from "@angular/core";
import { Milp_parameters } from "./milp_parameter.model";
import { Economic_dispatch } from "./economic_dispatch.model";
import { RestDataSource } from "./rest.datasource";

@Injectable()
export class Model {
    public milp_parameters: Milp_parameters[] = new Array<Milp_parameters>();
    public economic_dispatch: Economic_dispatch[] = new Array<Economic_dispatch>();
    private locator_Milp_parameters = (p: Milp_parameters, id: number) => p.id == id;
    private locator_Economic_dispatch = (p: Economic_dispatch, id: number) => p.id == id;

    constructor(private dataSource: RestDataSource) {
        this.dataSource.getData_Milp_parameters().subscribe(data => this.milp_parameters = data);
        this.dataSource.getData_Economic_dispatch().subscribe(data => this.economic_dispatch = data);
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
}
