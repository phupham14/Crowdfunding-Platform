import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: '', redirectTo: 'landing', pathMatch: 'full' },
  { path: 'landing', loadChildren: () => import('./features/landing/landing.module').then(m => m.LandingModule) },
  { path: 'auth', loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule) },
  { path: 'projects', loadChildren: () => import('./features/project-listing/project-listing.module').then(m => m.ProjectListingModule) },
  { path: 'project/:id', loadChildren: () => import('./features/project-detail/project-detail.module').then(m => m.ProjectDetailModule) },
  { path: 'risk-profiles', loadChildren: () => import('./features/risk-profile/risk-profile.module').then(m => m.RiskProfileModule)},
  { path: 'investor', loadChildren: () => import('./investor/investor.module').then(m => m.InvestorModule) },
  { path: 'project-owner', loadChildren: () => import('./features/project-owner/project-owner.module').then(m => m.ProjectOwnerModule)},
  { path: 'reports', loadChildren: () => import('./features/reports/reports.module').then(m => m.ReportsModule)},
  { path: 'transactions', loadChildren: () => import('./features/transaction/transaction.module').then(m => m.TransactionModule)},
  { path: 'admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) },
  { path: '**', redirectTo: 'landing' }
];
  
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
