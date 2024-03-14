import { Component, OnInit } from '@angular/core';
import { EV_parameters } from 'src/app/shared/model/ev_parameters.model';
import { Model } from 'src/app/shared/model/repository.model'; 
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-ev',
  templateUrl: './ev.component.html',
  styleUrls: ['./ev.component.scss']
})
export class EVComponent implements OnInit {

  constructor(private model: Model) { }

  ngOnInit(): void {  }

  newParameters: EV_parameters = new EV_parameters();

  addParameters(p: EV_parameters) {
    this.model.updateEVParameters(p)
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

    } else {

      this.validSubmission = false;
    
    }
  }
}

