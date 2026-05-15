# import logging
# _LOGGER = logging.getLogger(__name__)

from typing import Any

from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

from custom_components.ecoflow_cloud.api import EcoflowApiClient
from custom_components.ecoflow_cloud.devices import BaseDevice, const
from custom_components.ecoflow_cloud.devices.public import data_bridge
from custom_components.ecoflow_cloud.number import ChargingPowerEntity, MaxBatteryLevelEntity, MinBatteryLevelEntity
from custom_components.ecoflow_cloud.sensor import (
    AmpSensorEntity,
    FrequencySensorEntity,
    InWattsSensorEntity,
    LevelSensorEntity,
    MiscSensorEntity,
    OutWattsSensorEntity,
    QuotaScheduledStatusSensorEntity,
    RemainSensorEntity,
    VoltSensorEntity,
)
from custom_components.ecoflow_cloud.switch import EnabledEntity


class DeltaProUltra(BaseDevice):
    def sensors(self, client: EcoflowApiClient) -> list[SensorEntity]:
        return [
            # ── Main battery level ──────────────────────────────────────────────
            LevelSensorEntity(client, self, "hs_yj751_pd_appshow_addr.soc", const.MAIN_BATTERY_LEVEL)
            .attr("hs_yj751_bms_slave_addr.1.remainCap", const.ATTR_REMAIN_CAPACITY, 0)
            .attr("hs_yj751_bms_slave_addr.1.fullCap", const.ATTR_FULL_CAPACITY, 0)
            .attr("hs_yj751_bms_slave_addr.1.designCap", const.ATTR_DESIGN_CAPACITY, 0),

            # ── Total power (in / out) ──────────────────────────────────────────
            WattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.wattsInSum", const.TOTAL_IN_POWER),
            WattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.wattsOutSum", const.TOTAL_OUT_POWER),

            # ── Discharge remaining time ────────────────────────────────────────
            RemainSensorEntity(client, self, "hs_yj751_pd_appshow_addr.remainTime",
                               const.DISCHARGE_REMAINING_TIME),

            # ── AC ports ────────────────────────────────────────────────────────
            # 5.8 kW AC input port
            InWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.inAc5p8Pwr", const.AC_IN_POWER),
            # AC output – total and per-leg
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outAcTtPwr", const.AC_OUT_POWER),
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outAcL11Pwr", "AC Out L1-1 Power"),
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outAcL12Pwr", "AC Out L1-2 Power"),
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outAcL21Pwr", "AC Out L2-1 Power"),
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outAcL22Pwr", "AC Out L2-2 Power"),
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outAc5p8Pwr", "5.8kW Port Out Power"),

            # ── Solar (MPPT) ────────────────────────────────────────────────────
            InWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.inHvMpptPwr", "Solar HV In Power"),
            InWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.inLvMpptPwr", "Solar LV In Power"),

            # ── USB / Type-C ────────────────────────────────────────────────────
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outTypec1Pwr",
                                 const.TYPEC_1_OUT_POWER),
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outTypec2Pwr",
                                 const.TYPEC_2_OUT_POWER),
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outUsb1Pwr", const.USB_1_OUT_POWER),
            OutWattsSensorEntity(client, self, "hs_yj751_pd_appshow_addr.outUsb2Pwr", const.USB_2_OUT_POWER),

            # ── BMS backend ────────────────────────────────────────────────────
            WattsSensorEntity(client, self, "hs_yj751_pd_backend_addr.bmsOutputWatts", "BMS Output Power"),
            WattsSensorEntity(client, self, "hs_yj751_pd_backend_addr.bmsInputWatts", "BMS Input Power"),
            VoltSensorEntity(client, self, "hs_yj751_pd_backend_addr.batVol", const.BATTERY_VOLT, False),

            # ── Temperatures ────────────────────────────────────────────────────
            TempSensorEntity(client, self, "hs_yj751_pd_backend_addr.pcsAcTemp", "PCS Temperature"),
            TempSensorEntity(client, self, "hs_yj751_pd_backend_addr.pdTemp", "PD Temperature"),

            # ── Battery Pack 1 (hs_yj751_bms_slave_addr.1.*) ───────────────────
            LevelSensorEntity(client, self, "hs_yj751_bms_slave_addr.1.soc",
                              const.SLAVE_N_BATTERY_LEVEL % 1, False, True)
            .attr("hs_yj751_bms_slave_addr.1.remainCap", const.ATTR_REMAIN_CAPACITY, 0)
            .attr("hs_yj751_bms_slave_addr.1.fullCap", const.ATTR_FULL_CAPACITY, 0)
            .attr("hs_yj751_bms_slave_addr.1.designCap", const.ATTR_DESIGN_CAPACITY, 0),
            CapacitySensorEntity(client, self, "hs_yj751_bms_slave_addr.1.remainCap",
                                 const.SLAVE_N_REMAIN_CAPACITY % 1, False),
            CapacitySensorEntity(client, self, "hs_yj751_bms_slave_addr.1.fullCap",
                                 const.SLAVE_N_FULL_CAPACITY % 1, False),
            CapacitySensorEntity(client, self, "hs_yj751_bms_slave_addr.1.designCap",
                                 const.SLAVE_N_DESIGN_CAPACITY % 1, False),
            TempSensorEntity(client, self, "hs_yj751_bms_slave_addr.1.temp",
                             const.SLAVE_N_BATTERY_TEMP % 1, False, True),
            CyclesSensorEntity(client, self, "hs_yj751_bms_slave_addr.1.cycles",
                               const.SLAVE_N_CYCLES % 1, False),
            AmpSensorEntity(client, self, "hs_yj751_bms_slave_addr.1.amp",
                            const.SLAVE_N_BATTERY_CURRENT % 1, False),

            # ── Battery Pack 2 (hs_yj751_bms_slave_addr.2.*) ───────────────────
            LevelSensorEntity(client, self, "hs_yj751_bms_slave_addr.2.soc",
                              const.SLAVE_N_BATTERY_LEVEL % 2, False, True)
            .attr("hs_yj751_bms_slave_addr.2.remainCap", const.ATTR_REMAIN_CAPACITY, 0)
            .attr("hs_yj751_bms_slave_addr.2.fullCap", const.ATTR_FULL_CAPACITY, 0)
            .attr("hs_yj751_bms_slave_addr.2.designCap", const.ATTR_DESIGN_CAPACITY, 0),
            CapacitySensorEntity(client, self, "hs_yj751_bms_slave_addr.2.remainCap",
                                 const.SLAVE_N_REMAIN_CAPACITY % 2, False),
            CapacitySensorEntity(client, self, "hs_yj751_bms_slave_addr.2.fullCap",
                                 const.SLAVE_N_FULL_CAPACITY % 2, False),
            CapacitySensorEntity(client, self, "hs_yj751_bms_slave_addr.2.designCap",
                                 const.SLAVE_N_DESIGN_CAPACITY % 2, False),
            TempSensorEntity(client, self, "hs_yj751_bms_slave_addr.2.temp",
                             const.SLAVE_N_BATTERY_TEMP % 2, False, True),
            CyclesSensorEntity(client, self, "hs_yj751_bms_slave_addr.2.cycles",
                               const.SLAVE_N_CYCLES % 2, False),
            AmpSensorEntity(client, self, "hs_yj751_bms_slave_addr.2.amp",
                            const.SLAVE_N_BATTERY_CURRENT % 2, False),

            QuotaStatusSensorEntity(client, self),
        ]


    def numbers(self, client: EcoflowApiClient) -> list[NumberEntity]:
        return [
            MinBatteryLevelEntity(
                client,
                self,
                "hs_yj751_pd_app_set_info_addr.dsgMinSoc",
                const.MIN_DISCHARGE_LEVEL,
                0,
                30,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "YJ751_PD_DSG_SOC_MIN_SET",
                    "params": {"minDsgSoc": value},
                },
            ),
            MaxBatteryLevelEntity(
                client,
                self,
                "hs_yj751_pd_app_set_info_addr.chgMaxSoc",
                const.MAX_CHARGE_LEVEL,
                50,
                100,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "YJ751_PD_CHG_SOC_MAX_SET",
                    "params": {"maxChgSoc": value},
                },
            ),
            ChargingPowerEntity(
                client,
                self,
                "hs_yj751_pd_app_set_info_addr.chgC20SetWatts",
                const.AC_CHARGING_POWER,
                600,
                1800,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "YJ751_PD_AC_CHG_SET",
                    "params": {"chgC20Watts": value},
                },
            ).with_icon("mdi:power-plug"),
            ChargingPowerEntity(
                client,
                self,
                "hs_yj751_pd_app_set_info_addr.chg5p8SetWatts",
                const.PIO_PORT_CHARGING_POWER,
                600,
                7200,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "YJ751_PD_AC_CHG_SET",
                    "params": {"chg5p8Watts": value},
                },
            ),
        ]

    def switches(self, client: EcoflowApiClient) -> list[SwitchEntity]:
        return [
            EnabledEntity(
                client,
                self,
                "hs_yj751_pd_appshow_addr.wireless4gOn",
                const.WIRELESS_4G_ENABLED,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "YJ751_PD_4G_SWITCH_SET",
                    "params": {"en4GOpen": value},
                },
            ).with_icon("mdi:signal-4g"),
            EnabledEntity(
                client,
                self,
                "hs_yj751_pd_app_set_info_addr.bmsModeSet",
                const.BATTERY_AUTO_HEATING_ENABLED,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "YJ751_PD_BP_HEAT_SET",
                    "params": {"enBpHeat": value},
                },
            ).with_icon("mdi:thermometer-check"),
            EnabledEntity(
                client,
                self,
                "hs_yj751_pd_appshow_addr.showFlag.6",
                const.DC_MODE,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "YJ751_PD_DC_SWITCH_SET",
                    "params": {"enable": value},
                },
            ).with_icon("mdi:current-dc"),
        ]

    def selects(self, client: EcoflowApiClient) -> list[SelectEntity]:
        return []

    def _prepare_data(self, raw_data) -> dict[str, Any]:
        res = super()._prepare_data(raw_data)
        res = self.to_plain_nested_addr_prefix(res)

        # split showFlag into separate keys for each bit using documentation's bit ordering
        if "hs_yj751_pd_appshow_addr.showFlag" in res["params"] and isinstance(
            res["params"]["hs_yj751_pd_appshow_addr.showFlag"], int
        ):
            documentation_bit_order = ((res["params"]["hs_yj751_pd_appshow_addr.showFlag"] >> 4) & 3855) | (
                res["params"]["hs_yj751_pd_appshow_addr.showFlag"] << 4
            )
            for x in range(16):
                res["params"][f"hs_yj751_pd_appshow_addr.showFlag.{x + 1}"] = (documentation_bit_order >> x) & 1
        return res

    def to_plain_nested_addr_prefix(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        if "typeCode" in raw_data:
            prefix = data_bridge.status_to_plain.get(raw_data["typeCode"], "unknown_" + raw_data["typeCode"])
        elif "addr" in raw_data:
            prefix = raw_data["addr"]
        elif "cmdFunc" in raw_data and "cmdId" in raw_data:
            prefix = f"{raw_data['cmdFunc']}_{raw_data['cmdId']}"
        else:
            # Used for quota/all responses
            return raw_data

        new_params: dict[str, Any] = {}
        if "params" in raw_data:
            self.nested_to_top_level(new_params, prefix, raw_data["params"])
        if "param" in raw_data:
            self.nested_to_top_level(new_params, prefix, raw_data["param"])

        result: dict[str, Any] = {"params": new_params}
        for k, v in raw_data.items():
            if k != "param" and k != "params":
                result[k] = v
        return result

    def nested_to_top_level(self, dest: dict[str, Any], k: str, v: Any):
        """Converts each nested dict/list value to a top-level key of
        the prefix followed by dot notation path to the value.
        ex.
            {"a": [123, {"b": 456}]} -> {"a.0": 123, "a.1.b": 456}
        """
        if isinstance(v, dict):
            for kk, vv in v.items():
                self.nested_to_top_level(dest, f"{k}.{kk}", vv)
        elif isinstance(v, list):
            for ii, vv in enumerate(v):
                self.nested_to_top_level(dest, f"{k}.{ii}", vv)
        else:
            dest[k] = v
