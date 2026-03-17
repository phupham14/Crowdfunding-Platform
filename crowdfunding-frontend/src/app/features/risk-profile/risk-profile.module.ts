import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms'; // <-- import thêm  
import { RiskProfileComponent } from './risk-profile/risk-profile.component';
import { RiskProfileRoutingModule } from './risk-profile-routing.module';

@NgModule({
  declarations: [RiskProfileComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,  // <-- thêm vào đây
    RiskProfileRoutingModule
  ]
})
export class RiskProfileModule { }
