from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from starlette.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from odoo.api import Environment
from odoo.exceptions import AccessError, MissingError

from odoo_dep import odoo_env
from schemas import Partner


router = APIRouter(prefix="/partners",
                   tags=["partners"]
                   )


@router.get("", response_model=List[Partner])
def partners(is_company: Optional[bool] = None, env: Environment = Depends(odoo_env)):
    domain = []
    if is_company is not None:
        domain.append(("is_company", "=", is_company))
    partners = env["res.partner"].search(domain)
    return [Partner.from_res_partner(p) for p in partners]


@router.get("/{partner_id}", response_model=Partner)
def get_partner(partner_id: int, env: Environment = Depends(odoo_env)):
    try:
        partner = env["res.partner"].browse(partner_id)
        return Partner.from_res_partner(partner)
    except MissingError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    except AccessError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)


@router.post("", response_model=Partner, status_code=HTTP_201_CREATED)
def create_partner(partner: Partner, env: Environment = Depends(odoo_env)):
    vals = {"name": partner.name,
            "email": partner.email,
            "is_company": partner.is_company,
            }
    partner = env["res.partner"].create(vals)
    return Partner.from_res_partner(partner)
