import type { PresentationProfile } from "../../api";
import type { InvBody } from "../../investigation/parseInvestigation";
import { EngineerInvestigationWorkspace } from "./EngineerInvestigationWorkspace";
import { LeadInvestigationWorkspace } from "./LeadInvestigationWorkspace";
import { StakeholderInvestigationWorkspace } from "./StakeholderInvestigationWorkspace";

interface Props {
  profile: PresentationProfile;
  data: InvBody;
}

export function InvestigationWorkspace({ profile, data }: Props) {
  switch (profile) {
    case "lead":
      return <LeadInvestigationWorkspace data={data} />;
    case "stakeholder":
      return <StakeholderInvestigationWorkspace data={data} />;
    default:
      return <EngineerInvestigationWorkspace data={data} />;
  }
}
