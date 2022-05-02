import { Component, OnInit } from '@angular/core';
import { Milp_parameters } from 'src/app/shared/model/milp_parameter.model';
import { Model } from 'src/app/shared/model/repository.model'; 
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-posts',
  templateUrl: './posts.component.html',
  styleUrls: ['./posts.component.scss']
})
export class PostsComponent implements OnInit {

  public costsChart = new Array();

  constructor(private model: Model, private http: HttpClient) { 


    this.http.get<Milp_parameters>('http://10.144.246.154:8051/v1/api/milp_parameters/1/')
      .subscribe(
        data2 => {
          this.costsChart = [];
          this.costsChart.push(Number(data2.pcc_cost_t24));
          this.costsChart.push(Number(data2.pcc_cost_t01));
          this.costsChart.push(Number(data2.pcc_cost_t02));
          this.costsChart.push(Number(data2.pcc_cost_t03));
          this.costsChart.push(Number(data2.pcc_cost_t04));
          this.costsChart.push(Number(data2.pcc_cost_t05));
          this.costsChart.push(Number(data2.pcc_cost_t06));
          this.costsChart.push(Number(data2.pcc_cost_t07));
          this.costsChart.push(Number(data2.pcc_cost_t08));
          this.costsChart.push(Number(data2.pcc_cost_t09));
          this.costsChart.push(Number(data2.pcc_cost_t10));
          this.costsChart.push(Number(data2.pcc_cost_t11));
          this.costsChart.push(Number(data2.pcc_cost_t12));
          this.costsChart.push(Number(data2.pcc_cost_t13));
          this.costsChart.push(Number(data2.pcc_cost_t14));
          this.costsChart.push(Number(data2.pcc_cost_t15));
          this.costsChart.push(Number(data2.pcc_cost_t16));
          this.costsChart.push(Number(data2.pcc_cost_t17));
          this.costsChart.push(Number(data2.pcc_cost_t18));
          this.costsChart.push(Number(data2.pcc_cost_t19));
          this.costsChart.push(Number(data2.pcc_cost_t20));
          this.costsChart.push(Number(data2.pcc_cost_t21));
          this.costsChart.push(Number(data2.pcc_cost_t22));
          this.costsChart.push(Number(data2.pcc_cost_t23));
          // console.log(this.costsChart)
    });

  }

  ngOnInit() { }

  getParameters(): Milp_parameters[] {
    return this.model.getMilpParameters();
  }

  getParameter(key: number): Milp_parameters {
    return this.model.getMilpParameter(key);
  }

  newParameters: Milp_parameters = new Milp_parameters();

  // get jsonParameters() {
  //   return JSON.stringify(this.newParameters);
  // }

  addParameters(p: Milp_parameters) {
    this.model.updateMilpParameters(p)
    // console.log("New parameters: " + this.jsonParameters);
  }

  formSubmitted: boolean = false;
  validSubmission: boolean = false;

  submitForm(form: NgForm) {
    this.formSubmitted = true;
    if (form.valid) {
      this.newParameters.id = 1;
      this.addParameters(this.newParameters);

      form.reset;
      this.formSubmitted = false;
      this.validSubmission = true;

      this.costsChart = [];
      this.costsChart.push(Number(this.newParameters.pcc_cost_t01));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t02));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t03));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t04));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t05));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t06));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t07));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t08));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t09));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t10));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t11));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t12));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t13));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t14));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t15));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t16));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t17));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t18));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t19));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t20));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t21));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t22));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t23));
      this.costsChart.push(Number(this.newParameters.pcc_cost_t24));
      // console.log(this.costsChart)

    } else {

      this.validSubmission = false;
    
    }
  }
}
